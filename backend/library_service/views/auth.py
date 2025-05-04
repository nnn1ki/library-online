from aiohttp import ClientSession, ClientResponseError

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

from library_service.opac.api.login import login_reader, login_librarian, login_admin, AuthResponse

User = get_user_model()

class AuthViewset(AsyncAPIView):
    class Serializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:
            try:
                response = await login_reader(client, serializer.validated_data["username"], serializer.validated_data["password"])
            except ClientResponseError as error:
                print(error)
