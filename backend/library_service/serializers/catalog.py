from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from library_service.irbis.book import Book
from library_service.models.catalog import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "description", "address"]

class BookSerializer(DataclassSerializer):
    class Meta:
        dataclass = Book