from rest_framework import serializers
from rest_framework.exceptions import APIException

from library_service.opac.book import book_retrieve
from library_service.models.order import *
from library_service.models.catalog import Library

from library_service.serializers.catalog import BookSerializer, LibrarySerializer

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date"]

class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ["id", "book", "handed", "returned"]

    def get_book(self, obj: OrderItem):
        return BookSerializer(book_retrieve(obj.book_id)).data

class OrderSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books"]


class CreateUpdateOrderSerializer(serializers.Serializer):
    library = serializers.IntegerField()
    books = serializers.ListField(child=serializers.CharField())
    borrowed = serializers.ListField(child=serializers.IntegerField())

    def configure_order(self, order: Order, validated_data):
        books: list[str] = validated_data["books"]
        for book in books:
            # TODO: проверка валидности айдишников
            # TODO: exemplar_id
            OrderItem.objects.create(order=order, book_id=book)

        borrowed_books: list[str] = validated_data["borrowed"] # Здесь список айдишников из OrderItem
        for book in borrowed_books:
            order_item = OrderItem.objects.get(pk=book)
            if order_item is not None and order_item.order == order and order_item.handed and not order_item.returned:
                order_item.order_to_return = order
                order_item.save()

    def create(self, validated_data):
        user = self.context["request"].user

        order = Order.objects.create(user=user, library=Library.objects.get(pk=validated_data["library"]))
        self.configure_order(order, validated_data)

        OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)
        return validated_data

    def update(self, instance: Order, validated_data):
        order_statuses = OrderHistory.objects.filter(order=instance).all()
        
        # Когда статус new, то в истории статусов заказа будет только одна запись
        if (order_statuses.count() > 1):
            raise APIException("Order status is not new", code=400)
        
        OrderItem.objects.filter(order=instance).all().delete()

        old_borrowed_books = OrderItem.objects.filter(order_to_return=instance).all()
        for order_item in old_borrowed_books:
            order_item.order_to_return = None
            order_item.save()
        
        instance.library = Library.objects.get(pk=validated_data["library"])
        instance.save()

        self.configure_order(instance, validated_data)
        # TODO: как-то помечать, что заказ был изменен?
        return validated_data


class BorrowedBookSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order"]
    
    def get_book(self, obj: OrderItem):
        return BookSerializer(book_retrieve(obj.book_id)).data