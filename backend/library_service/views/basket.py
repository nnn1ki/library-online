import asyncio
from aiohttp import ClientSession
from django.http import Http404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.mixins import SessionCreateModelMixin
from library_service.models.user import BasketItem
from library_service.serializers.basket import AddBasketSerializer
from library_service.serializers.catalog import BookSerializer
from library_service.opac.book import book_retrieve


class BasketViewset(SessionCreateModelMixin, amixins.DestroyModelMixin, AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

    def get_serializer_class(self):
        if self.action in ["acreate", "replace"]:
            return AddBasketSerializer
        else:
            return BookSerializer

    def get_queryset(self):
        return super().get_queryset().filter(basket__user=self.request.user)

    async def aget_object(self):
        pk = self.kwargs["pk"]
        item = await self.get_queryset().filter(book_id=pk).afirst()

        if item is None:
            raise Http404("Book not found")

        return item

    async def alist(self, request, *args, **kwargs):
        async with ClientSession() as client:
            books = await asyncio.gather(*[book_retrieve(client, book.book_id) async for book in self.get_queryset()])
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

    @action(detail=False, url_path="replace", methods=["put"])
    async def replace(self, request, *args, **kwargs):
        await self.get_queryset().adelete()
        return await self.acreate(request, *args, **kwargs)
