from rest_framework import serializers

from library_service.models.order import *
from library_service.serializers.catalog import LibrarySerializer

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date"]

class OrderBookSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="exemplar_id") # TODO: retrieve_book

    class Meta:
        model = OrderItem
        fields = ["id", "book", "handed", "returned"]

class OrderSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderBookSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books"]

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="exemplar_id") # TODO: retrieve_book

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order"]