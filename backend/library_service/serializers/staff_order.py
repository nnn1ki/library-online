from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.models.user import UserProfile
from library_service.opac.book import book_retrieve

from library_service.serializers.catalog import BookSerializer, LibrarySerializer
from library_service.serializers.parallel_list import ParallelListSerializer

from library_service.opac.api.ticket import OpacLoan
from library_service.opac.api.ticket import opac_reader_loans
from library_service.opac.book import book_retrieve_by_id

from aiohttp import ClientSession

User = get_user_model()

class StaffOrderSerializer(aserializers.ModelSerializer):
    campus_id = serializers.CharField(source="profile.campus_id", read_only=True)
    mira_id = serializers.CharField(source="profile.mira_id", read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "campus_id", "mira_id"]

class OrderStatusSerializer(aserializers.ModelSerializer):
    staff = StaffOrderSerializer()

    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date", "staff"]

class OrderUserSerializer(aserializers.ModelSerializer):
    library_card = serializers.CharField(source="profile.library_card", read_only=True)
    campus_id = serializers.CharField(source="profile.campus_id", read_only=True)
    mira_id = serializers.CharField(source="profile.mira_id", read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "library_card", "campus_id", "mira_id"]


class OrderItemSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "status",
            "handed_date",
            "to_return_date",
            "returned_date",
        ]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data


class OrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderItemSerializer(many=True)
    user = OrderUserSerializer()

    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books", "user"]
        list_serializer_class = ParallelListSerializer


class UserOrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    user = OrderUserSerializer()

    class Meta:
        model = Order
        fields = ["id", "user", "library", "statuses"]
        list_serializer_class = ParallelListSerializer

class OrderBookSerializer(serializers.ModelSerializer): 

    class Meta:
        model = OrderItem
        fields = ["id", "exemplar_id" "status", "description", "analogous_order_item_id"]
        list_serializer_class = ParallelListSerializer

class UpdateOrderSerializer(aserializers.Serializer):
    status = OrderStatusSerializer()
    books = OrderBookSerializer(many=True)

    async def aupdate(self, instance: Order, validated_data):
        user = self.context["request"].user
        new_status = validated_data["status"]

        if (new_status["status"] == OrderHistory.Status.PROCESSING):
            await OrderHistory.objects.acreate(
                order=instance, 
                status=OrderHistory.Status.PROCESSING,
                description=new_status["description"],
                staff=user
            )
            
        elif (new_status["status"] == OrderHistory.Status.NEW):
            await OrderHistory.objects.acreate(
                order=instance, 
                status=OrderHistory.Status.NEW,
                description=new_status["description"],
                staff=user
            )
            
        elif (new_status["status"] == OrderHistory.Status.READY):
            order_books = validated_data["books"]

            # async for order_item in order_books:
            #     if validated_data["exemplar_id"] is not None:
            #         order_item.exemplar_id = validated_data["exemplar_id"]
                
            #     if validated_data["analogous_order_item"] is not None:
            #         analogous_order_item = await OrderItem.objects.acreate(
            #             order = instance,
            #             book_id = validated_data["analogous_order_item"]["book_id"],
            #             exemplar_id = validated_data["analogous_order_item"]["exemplar_id"],
            #             status = OrderItem.Status.ORDERED
            #         )

            #         order_item.analogous_order_item = analogous_order_item
                
            #     await order_item.asave()

            await OrderHistory.objects.acreate(
                order=instance, 
                status=OrderHistory.Status.READY,
                description=new_status["description"],
                staff=user
            )
            
        elif (new_status["status"] == OrderHistory.Status.DONE):

            #TODO: нужно проверять какие книги сотрудник пропи кал по итогу, и уже с ними работать

            await OrderHistory.objects.acreate(
                order=instance, 
                status=OrderHistory.Status.DONE,
                description=new_status["description"],
                staff=user
            )

        elif (new_status["status"] == OrderHistory.Status.CANCELLED):
            order_items_list: list[OrderItem] = OrderItem.objects.filter(order = instance).all()

            async for order_item in order_items_list:
                order_item.status = OrderItem.Status.CANCELLED
                await order_item.asave()

                if (order_item.analogous_order_item is not None):
                    await OrderItem.objects.filter(id = order_item.analogous_order_item.id).adelete()
                
            items_to_return: list[OrderItem] = OrderItem.objects.filter(order_to_return = instance).all()

            async for order_item in items_to_return:
                order_item.order_to_return = None
                await order_item.asave()

            await OrderHistory.objects.acreate(
                order=instance, 
                status=OrderHistory.Status.CANCELLED,
                description=new_status["description"],
                staff=user
            )

        return validated_data
    

class BorrowedBookSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order", "handed_date", "to_return_date"]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data
    
class CheckOrderSerializer(aserializers.Serializer):
    found_books = OrderItemSerializer(many = True)
    notfound_books = OrderItemSerializer(many = True)
    additional_books = serializers.ListField(child=serializers.CharField())
