import asyncio
from aiohttp import ClientSession
from rest_framework import serializers
from rest_framework.exceptions import APIException

from adrf import serializers as aserializers

from library_service.models.user import Basket, BasketItem
from library_service.opac.book import book_validate

class AddBasketSerializer(aserializers.Serializer):
    books = serializers.ListField(child=serializers.CharField())

    async def acreate(self, validated_data):
        user = self.context["request"].user
        basket = await Basket.objects.filter(user=user).afirst()

        if (basket is None):
            basket = await Basket.objects.acreate(user=user)
        
        books_current = [book.book_id async for book in BasketItem.objects.filter(basket=basket)]
        books_add: list[str] = validated_data["books"]

        tasks = []
        for book in set(books_add):
            if book not in books_current:
                async def task(book=book):
                    if await book_validate(self.context["client_session"], book) is None:
                        raise APIException(f"Invalid book id {book}", code=400)
                    books_current.append(book)
                    await BasketItem.objects.acreate(book_id=book, basket=basket)
                tasks.append(task())
    
        await asyncio.gather(*tasks)            
        return {
            "books": books_current
        }
        
