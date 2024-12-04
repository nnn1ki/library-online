from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.irbis.book import books_list
from library_service.serializers.catalog import *
from library_service.models.catalog import *

class BookViewset(GenericViewSet):
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        library: str = self.request.query_params.get("library")
        name: str = self.request.query_params.get("name")
        author: str = self.request.query_params.get("author")

        libraries = Library.objects.all()
        if library is not None:
            libraries = libraries.filter(id=int(library))
        
        books = books_list(libraries, name, author)
        serializer = self.get_serializer(books, many=True)

        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
    @action(url_path="announcement", methods=["GET"], detail=False)
    def announcements_list(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
class LibraryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
