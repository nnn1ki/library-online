from rest_framework_dataclasses.serializers import DataclassSerializer

from adrf import serializers as aserializers

from library_service.models.catalog import Library
from library_service.opac.api.scenarios import OpacScenario
from library_service.opac.book import Book


class LibrarySerializer(aserializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "description", "address"]


class BookSerializer(DataclassSerializer):
    class Meta:
        dataclass = Book


class ScenarioSerializer(DataclassSerializer):
    class Meta:
        dataclass = OpacScenario
