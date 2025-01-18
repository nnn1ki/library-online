from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.irbis.book import Book
from library_service.serializers.basket import *
from library_service.models.catalog import *

from rest_framework.permissions import IsAuthenticated

from library_service.irbis.book import book_retrieve

class BasketViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer

    @action(methods=["GET"], detail = False,  permission_classes = [IsAuthenticated])
    def get_queryset(self):
        user_id = self.request.user.id
        return user_id
    
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @action(methods=["DELETE"], url_path="<book_id>", detail = False,  permission_classes = [IsAuthenticated])
    def delete_book(self, request, *args, **kwargs):
        #TODO
        return True