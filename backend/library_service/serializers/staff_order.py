import asyncio
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.opac.book import book_retrieve, book_retrieve_safe
from library_service.models.catalog import Library

from library_service.serializers.catalog import BookSerializer, LibrarySerializer
from library_service.serializers.parallel_list import ParallelListSerializer

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

    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books"]
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
    book_id = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ["book_id", "status", "description", "analogous_order_item_id"]
        list_serializer_class = ParallelListSerializer

class UpdateOrderSerializer(aserializers.Serializer):
    status = OrderStatusSerializer()
    books = OrderBookSerializer(many=True)

    async def aupdate(self, instance: Order, validated_data):
        user = self.context["request"].user
        new_status = validated_data["status"]

        if (new_status["status"] == OrderHistory.Status.PROCESSING):
            await OrderHistory.objects.acreate(order=instance, status=OrderHistory.Status.PROCESSING, description=new_status["description"], staff=user)
        elif (new_status["status"] == OrderHistory.Status.READY):
            order_books = validated_data["books"]

            # async for order_item in :
            #     order_item.order_to_return = None
            #     await order_item.asave()

            # instance.library = await Library.objects.aget(pk=validated_data["library"])
            # await instance.asave()

        return validated_data