from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.irbis.book import Book
from library_service.serializers.basket import *
from library_service.models.catalog import *

from rest_framework.permissions import IsAuthenticated

from library_service.irbis.book import book_retrieve

from rest_framework.exceptions import APIException

class BasketViewset(
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = BasketListSerializer
    query_data: list[int] | None = None

    @action(methods=["GET"], detail = False,  permission_classes = [IsAuthenticated])
    def get_queryset(self):
        user = self.request.user

        book_list = []

        if (user.is_authenticated):
            self.query_data = BasketListSerializer.get_basket(self)

            if (self.query_data.count() > 0):
                for book_id in self.query_data:
                    book = book_retrieve(book_id)
                    book_list.append(book)

        else:
            raise APIException("Unauthorized", code=401)

        return book_list
    
    @action(methods=["POST"], detail = False,  permission_classes = [IsAuthenticated])
    def add_books(self):
        user = self.request.user

        if (user.is_authenticated):
            BasketListSerializer.add_books(self.request.data)
        else:
            raise APIException("Unauthorized", code=401)    
    
    @action(methods=["PUT"], detail = False,  permission_classes = [IsAuthenticated])
    def update_basket(self):
        user = self.request.user

        if (user.is_authenticated):
            basket_list = self.get_queryset()
            books_to_delete = self.request.data

            for book in basket_list:
                if (book in books_to_delete):
                    self.request.data = book.id
                    BasketItemViewset.destroy(self.request)
        else:
            raise APIException("Unauthorized", code=401)    
    
    def destroy(self, request, *args, **kwargs):
        user = request.user

        if (user.is_authenticated):
            BasketItemViewset.destroy(request, *args, **kwargs)
        else:
            raise APIException("Unauthorized", code=401)    
    
class BasketItemViewset(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()