from django.http import Http404
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from library_service.serializers.basket import *
from library_service.serializers.catalog import BookSerializer
from library_service.irbis.book import book_retrieve

class BasketViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookSerializer
        elif self.action in ["create", "replace"]:
            return AddBasketSerializer
    
    def get_queryset(self):
        basket = Basket.objects.filter(user=self.request.user).first()
        return super().get_queryset().filter(basket=basket)

    def get_object(self):
        id = self.kwargs["pk"]
        object = self.get_queryset().filter(book_id=id)

        if object.count() == 0:
            raise Http404("Book not found")
        
        return object
    
    def list(self, request, *args, **kwargs):
        books = [book_retrieve(book.book_id) for book in self.get_queryset()]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="replace", methods=["put"])
    def replace(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return self.create(request, *args, **kwargs)