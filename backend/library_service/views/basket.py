import asyncio

from aiohttp import ClientSession
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.serializers.basket import *
from library_service.serializers.catalog import BookSerializer
from library_service.opac.book import book_retrieve

class BasketViewset(
    amixins.CreateModelMixin,
    amixins.DestroyModelMixin,
    AsyncGenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

    def get_serializer_class(self):
        if self.action == "alist":
            return BookSerializer
        elif self.action in ["acreate", "replace"]:
            return AddBasketSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(basket__user=self.request.user)

    async def aget_object(self):
        id = self.kwargs["pk"]
        object = self.get_queryset().filter(book_id=id)

        if await object.acount() == 0:
            raise Http404("Book not found")
        
        return object
    
    async def alist(self, request, *args, **kwargs):
        async with ClientSession() as client:
            books = await asyncio.gather(*[book_retrieve(client, book.book_id) async for book in self.get_queryset()])
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

    @action(detail=False, url_path="replace", methods=["put"])
    async def replace(self, request, *args, **kwargs):
        await self.get_queryset().adelete()
        return await self.acreate(request, *args, **kwargs)