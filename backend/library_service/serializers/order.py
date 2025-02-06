import asyncio
from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import APIException

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.opac.book import book_retrieve, book_validate
from library_service.models.order import *
from library_service.models.catalog import Library

from library_service.serializers.catalog import BookSerializer, LibrarySerializer

class OrderStatusSerializer(aserializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date"]

class OrderItemSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ["id", "book", "status", "handed_date", "to_return_date", "returned_date"]

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data

class OrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books"]


class CreateUpdateOrderSerializer(aserializers.Serializer):
    library = serializers.IntegerField()
    books = serializers.ListField(child=serializers.CharField())
    borrowed = serializers.ListField(child=serializers.IntegerField())

    async def configure_order(self, order: Order, validated_data):
        books: list[str] = validated_data["books"]
        if len(books) == 0:
            raise APIException(f"Can't make an empty order", code=400)

        current_books = [order_book.book_id async for order_book in OrderItem.objects.all().filter(order__user=self.context["request"].user).filter(Q(status=OrderItem.Status.ORDERED) | Q(status=OrderItem.Status.HANDED))]
        tasks = []
        for book_id in set(books):
            async def task(book_id=book_id):
                if book_id in current_books:
                    raise APIException(f"Can't order the same book {book_id} twice", code=400)

                book = await book_validate(self.context["client_session"], book_id, order.library)

                if book is None:
                    raise APIException(f"Invalid book id {book_id}", code=400)
                
                if not book.can_be_ordered:
                    raise APIException(f"Can't order book {book_id}", code=400)

                # TODO: exemplar_id
                await OrderItem.objects.acreate(order=order, book_id=book_id)
            tasks.append(task())
        
        await asyncio.gather(*tasks)

        borrowed_books: list[str] = validated_data["borrowed"]
        for book in borrowed_books:
            order_item = await OrderItem.objects.aget(pk=book)
            if order_item is not None and order_item.order == order and order_item.status == OrderItem.Status.HANDED:
                order_item.order_to_return = order
                await order_item.asave()

    async def acreate(self, validated_data):
        user = self.context["request"].user

        order = await Order.objects.acreate(user=user, library=await Library.objects.aget(pk=validated_data["library"]))
        await self.configure_order(order, validated_data)

        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.NEW)
        return validated_data

    async def aupdate(self, instance: Order, validated_data):
        order_statuses = OrderHistory.objects.filter(order=instance).all()
        
        # Когда статус new, то в истории статусов заказа будет только одна запись
        if (await order_statuses.acount() > 1):
            raise APIException("Order status is not new", code=400)
        
        await OrderItem.objects.filter(order=instance).all().adelete()

        old_borrowed_books = OrderItem.objects.filter(order_to_return=instance).all()
        async for order_item in old_borrowed_books:
            order_item.order_to_return = None
            await order_item.asave()
        
        instance.library = await Library.objects.aget(pk=validated_data["library"])
        await instance.asave()

        await self.configure_order(instance, validated_data)
        # TODO: как-то помечать, что заказ был изменен?
        return validated_data


class BorrowedBookSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order", "handed_date", "to_return_date"]
    
    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data