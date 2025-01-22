from rest_framework import serializers

from library_service.models.user import Basket, BasketItem

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
                # TODO: проверка валидности айдишников?
                BasketItem.objects.create(book_id=book, basket=basket)
                books_current.append(book)

        return {
            "books": books_current
        }

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["book_id"]