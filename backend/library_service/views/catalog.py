from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.irbis.api.scenarios import irbis_scenarios
from library_service.irbis.book import books_announces_list, books_list, Book
from library_service.serializers.catalog import *
from library_service.models.catalog import *

class BookViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = BookSerializer
    query_data: list[Book] | None = None

    def get_queryset(self):
        if self.query_data is None:
            library: str = self.request.query_params.get("library")
            name: str = self.request.query_params.get("name")
            author: str = self.request.query_params.get("author")

            libraries = Library.objects.all()
            if library is not None:
                libraries = libraries.filter(id=int(library))
            
            self.query_data = books_list(libraries, name, author)

        return self.query_data

    def get_object(self):
        # TODO: разобраться с этим
        raise NotImplementedError("В их апи нет возможности получения книги по id 🤗")

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
    query_data: list[IrbisScenario] | None = None

    def get_queryset(self):
        if self.query_data is None:           
            self.query_data = irbis_scenarios("ISTU") # TODO: убрать хардкод

        return self.query_data