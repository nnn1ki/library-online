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
    basket_item = BasketItemSerializer

    def get_basket(self):
        basket_id = Basket.objects.filter(user = self.context["request"].user).values_list('id', flat = True).first()
        books_list = BasketItem.objects.filter(basket = basket_id).values_list('book_id', flat = True)
        return books_list
    
    def add_books(self, books):
        basket = Basket.objects.filter(user = self.context["request"].user).first()

        if (basket is None):
            basket = self.create()

        basket_item_validated_data = {
            "basket": basket,
            "book_id": 0
        }

        basket_list = self.get_basket()

        for book in books:
            if (book not in basket_list):
                basket_item_validated_data["book_id"] = book
                self.basket_item.create(basket_item_validated_data)

    def create(self):
        basket_validated_data = {
            "user": self.context["request"].user
        }

        created_basket_data = self.basket.create(basket_validated_data)

        return created_basket_data