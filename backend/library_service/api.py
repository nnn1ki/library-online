from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from library_service.models import *

from serializers import *

class BookViewset(mixins.ListModelMixin, GenericViewSet):
    serializer_class = BookSerializer

    @action(methods=["GET"], detail=False)
    def get_books_list(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
    @action(url_path="<str: id>", methods=["GET"], detail=False)
    def get_book_info(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
    @action(url_path="announcment", methods=["GET"], detail=False)
    def get_announcements_list(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
class LibraryViewset(mixins.ListModelMixin, GenericViewSet):
    serializer_class = LibrarySerializer

    action(methods=["GET"], detail=False)
    def get_libraries_list(self, request, *args, **kwargs):
         
        #TO-DO

        return Response()
    
    action(url_path="<str: name>", methods=["GET"], detail=False)
    def get_library_info(self, request, *args, **kwargs):

        #TO-DO

        return Response()