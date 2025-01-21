from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from library_service.irbis.book import Book
from library_service.models.user import Basket, BasketItem

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "created_at", "user"]

    def create(self, validated_data):
        return Basket.objects.create(**validated_data)

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["id", "book_id", "basket"]

    def create(self, validated_data):
        return BasketItem.objects.create(**validated_data)
    
    def delete(id):
        BasketItem.objects.filter(id = id).delete()
    
class BasketListSerializer(serializers.Serializer):
    basket = BasketSerializer
    basket_item = BasketItemSerializer
    
    def add_books(self, books):
        basket = Basket.objects.filter(user = self.request.user).first()

        if (basket is None):
            basket = BasketListSerializer.create(self)

        basket_item_validated_data = {
            "basket": basket,
            "book_id": 0
        }

        basket_list = BasketListSerializer.get_basket(self)

        for book in books:
            if (book not in basket_list):
                basket_item_validated_data["book_id"] = book
                BasketListSerializer.basket_item.create(self, basket_item_validated_data)

    def create(self):
        basket_validated_data = {
            "user": self.request.user
        }

        created_basket_data = BasketListSerializer.basket.create(self, basket_validated_data)

        return created_basket_data
    
    def delete_book(self, book_id):
        basket = Basket.objects.filter(user = self.request.user).first()

        basket_item = BasketItem.objects.filter(basket = basket, book_id = book_id).first()

        BasketListSerializer.basket_item.delete(basket_item.id)

class BookListSerializer(DataclassSerializer):
    class Meta:
        dataclass = Book