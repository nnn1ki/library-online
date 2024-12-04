from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins

from library_service.serializers.catalog import *
from library_service.models.catalog import *

class BookViewset(GenericViewSet):
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):

        #TO-DO

        return Response()
    
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
