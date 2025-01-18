from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from library_service.irbis.api.scenarios import IrbisScenario
from library_service.irbis.book import Book
from library_service.models.user import Basket, BasketItem

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "created_at", "user_id"]

    def create(self, validated_data):
        return super().create(validated_data)

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["id", "book_id", "basket_id"]

    def create(self, validated_data):
        return super().create(validated_data)
    
class BasketListSerializer(serializers.Serializer):
    basket = BasketSerializer
    items_list = BasketItemSerializer(many = True)

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)