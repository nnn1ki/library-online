from rest_framework import serializers

from rest_framework_dataclasses.serializers import DataclassSerializer

from library_service.models.order import *
from library_service.serializers.catalog import LibrarySerializer

from library_service.models.catalog import Library

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

class CreateOrderSerializer(serializers.Serializer):
    library = serializers.IntegerField()
    books = serializers.ListField(child = serializers.CharField())
    borrowed = serializers.ListField(child = serializers.IntegerField())

    def create(self, validated_data):
        user = self.context["request"].user
        library = Library.objects.get(pk = validated_data["library"])

        order = Order.objects.create(user = user, library = library)

        exemplars: list[str] = validated_data["books"]

        for exemplar in exemplars:
            OrderItem.objects.create(order = order, exemplar_id = exemplar)

        order_status = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW)

        borrowed_books: list[str] = validated_data["borrowed"] #Здесь список айдишников из Orderitem

        if (borrowed_books.count() > 0):
            for book in borrowed_books:
                order_item = OrderItem.objects.get(pk=book)
                if (order_item is not None):
                    order_item.order_to_return = order
                    order_item.save()
        
        return order