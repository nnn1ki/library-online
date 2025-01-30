from rest_framework import serializers
from rest_framework.exceptions import APIException

from library_service.models.user import Basket, BasketItem
from library_service.opac.book import book_validate

class AddBasketSerializer(serializers.Serializer):
    books = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        user = self.context["request"].user
        basket = Basket.objects.filter(user=user).first()

        if (basket is None):
            basket = Basket.objects.create(user=user)
        
        books_current = [book.book_id for book in BasketItem.objects.filter(basket=basket)]
        books_add: list[str] = validated_data["books"]
        for book in books_add:
            if book not in books_current:
                if book_validate(book) is None:
                    raise APIException(f"Invalid book id {book}", code=400)

                BasketItem.objects.create(book_id=book, basket=basket)
                books_current.append(book)

        return {
            "books": books_current
        }