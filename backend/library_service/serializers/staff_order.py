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

class OrderStatusSerializer(aserializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date"]


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