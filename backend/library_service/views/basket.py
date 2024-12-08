from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.irbis.book import Book
from library_service.serializers.catalog import *
from library_service.models.catalog import *

class BasketViewset(
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    serializer_class = BookSerializer
    query_data: list[Book] | None = None

    def get_queryset(self):
        return super().get_queryset()
    
    
    
    