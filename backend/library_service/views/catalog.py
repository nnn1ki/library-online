from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from rest_framework.exceptions import APIException

from library_service.opac.api.scenarios import opac_scenarios
from library_service.opac.book import book_retrieve, books_announces_list, books_list, Book
from library_service.serializers.catalog import *
from library_service.models.catalog import *

class BookViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = BookSerializer
    query_data: list[Book] | None = None

    def get_queryset(self):
        if self.query_data is None:
            library: str | None = self.request.query_params.get("library")
            expression: str | None = self.request.query_params.get("expression")

            if expression is None:
                raise APIException("No expression provided", code=400)

            libraries = Library.objects.all()
            if library is not None:
                libraries = libraries.filter(id=int(library))
            
            self.query_data = books_list(libraries, expression)

        return self.query_data

    def get_object(self):
        id = self.kwargs["pk"]
        book = book_retrieve(id)
        return book

    @action(url_path="announcement", methods=["GET"], detail=False)
    def announcements_list(self, request, *args, **kwargs):
        books = books_announces_list()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
class LibraryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class ScenarioViewset(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ScenarioSerializer
    query_data: list[OpacScenario] | None = None

    def get_queryset(self):
        if self.query_data is None:           
            self.query_data = opac_scenarios("ISTU") # TODO: по идее, сценарии сильно не отличаются между БД, но лучше все же убрать хардкод

        return self.query_data