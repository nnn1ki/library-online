from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.serializers.basket import *
from library_service.models.catalog import *

from library_service.irbis.book import book_retrieve

from rest_framework.exceptions import APIException

from rest_framework import status

class BasketViewset(
    mixins.ListModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
    mixins.CreateModelMixin
):
    def get_serializer_class(self):
        if (self.action == "list"):
            return BookListSerializer
        else:
            return BasketListSerializer

    def get_queryset(self):
        user = self.request.user

        if (user.is_authenticated):
            book_list = []

            basket = Basket.objects.filter(user = self.request.user).first()
            books = BasketItem.objects.filter(basket = basket).values_list("book_id", flat = True).all()

            if (books.count() > 0):
                for book in books:
                    book = book_retrieve(book)
                    book_list.append(book)

            return book_list

        else:
            raise APIException("Unauthorized", code=401)
    
    def create(self, request, *args, **kwargs):
        user = request.user

        if (user.is_authenticated):
            BasketListSerializer.add_books(self, request.data["books"])

            return Response(status = status.HTTP_200_OK)
        else:
            raise APIException("Unauthorized", code=401)    
    
    def update(self, request, *args, **kwargs):
        user = request.user

        if (user.is_authenticated):
            basket_list = self.get_queryset()
            update_list = list(request.data["books"])

            for book in basket_list:
                if (book not in update_list):
                    self.request.data = book.id
                    BasketViewset.destroy(request, *args, **kwargs)
                else:
                    update_list.remove(book)

            for book in update_list:
                BasketListSerializer.add_books(book)

            return Response(status=status.HTTP_200_OK)
                
        else:
            raise APIException("Unauthorized", code=401)    
    
    def destroy(self, request, *args, **kwargs):
        user = request.user

        if (user.is_authenticated):
            id = kwargs["pk"]
            BasketListSerializer.delete_book(self, id)
            return Response(status=status.HTTP_200_OK)
        else:
            raise APIException("Unauthorized", code=401)    