from aiohttp import ClientSession
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.models.catalog import Library
from library_service.opac.api.scenarios import opac_scenarios
from library_service.opac.book import book_retrieve_safe, books_announces_list, books_list
from library_service.serializers.catalog import BookSerializer, LibrarySerializer, ScenarioSerializer


class BookViewset(amixins.RetrieveModelMixin, AsyncGenericViewSet):
    serializer_class = BookSerializer

    # TODO: по идее, можно использовать миксин, но тогда придется реализовать ленивый get_queryset
    async def alist(self, request, *args, **kwargs):
        library: str | None = self.request.query_params.get("library")
        expression: str | None = self.request.query_params.get("expression")

        if expression is None:
            raise ValidationError("No expression provided", code="no_expression")

        libraries = Library.objects.all()
        if library is not None:
            libraries = libraries.filter(id=int(library))

        async with ClientSession() as client:
            books = await books_list(client, libraries, expression)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)

    async def aget_object(self):
        pk = self.kwargs["pk"]
        async with ClientSession() as client:
            book = await book_retrieve_safe(client, pk)
            if book is None:
                raise NotFound(f"Book {pk} not found", "book_not_found")
            return book

    @action(url_path="announcement", methods=["GET"], detail=False)
    async def announcements_list(self, request, *args, **kwargs):
        async with ClientSession() as client:
            books = await books_announces_list(client)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)


class LibraryViewset(amixins.ListModelMixin, amixins.RetrieveModelMixin, AsyncGenericViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class ScenarioViewset(AsyncGenericViewSet):
    serializer_class = ScenarioSerializer

    async def alist(self, request, *args, **kwargs):
        async with ClientSession() as client:
            # TODO: по идее, сценарии сильно не отличаются между БД, но лучше все же убрать хардкод
            scenarios = await opac_scenarios(client, "ISTU")
            serializer = self.get_serializer(scenarios, many=True)
            return Response(serializer.data)
