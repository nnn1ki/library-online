from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer

from library_service.opac.api.scenarios import OpacScenario
from library_service.opac.book import Book
from library_service.models.catalog import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "description", "address"]

class BookSerializer(DataclassSerializer):
    class Meta:
        dataclass = Book

class ScenarioSerializer(DataclassSerializer):
    class Meta:
        dataclass = OpacScenario