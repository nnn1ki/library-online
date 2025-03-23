import asyncio
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.opac.book import book_retrieve, book_retrieve_safe
from library_service.models.catalog import Library

from library_service.serializers.catalog import BookSerializer, LibrarySerializer
from library_service.serializers.parallel_list import ParallelListSerializer

User = get_user_model()

#class GetOrderSerializer(serializers.Serializer):
