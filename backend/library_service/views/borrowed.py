from django.http import Http404
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from library_service.serializers.catalog import BookSerializer
from library_service.irbis.book import book_retrieve

class BorrowedViewset (
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]