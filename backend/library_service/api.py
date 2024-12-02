from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from library_service.models import *

from serializers import *

# TODO: создать директорию views для логического разделения вьюсетов по файлам (эти вьюсеты можно поместить в один файл)

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
    
class LibraryViewset(GenericViewSet):
    serializer_class = LibrarySerializer

    def list(self, request, *args, **kwargs):
         
        #TO-DO

        return Response()
    
    def retrieve(self, request, *args, **kwargs):

        #TO-DO

        return Response()