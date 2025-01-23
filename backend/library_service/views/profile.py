from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library_service.models.user import UserProfile
from library_service.serializers.profile import *

class ProfileViewset(GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.all().filter(user=self.request.user)

    @action(detail=False, url_path="self-info", methods=["get"])
    def get_self(self, request, *args, **kwargs):
        profile = self.get_queryset().first()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)