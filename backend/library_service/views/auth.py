from aiohttp import ClientSession, ClientResponseError
from django.http import Http404

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

from library_service.opac.api.login import login_reader, login_librarian, login_admin, get_login_info, AuthResponse, UserInfo

User = get_user_model()

class AuthViewset(AsyncAPIView):
    class Serializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = await User.objects.filter(username = serializer.validated_data["username"]).afirst()

        #TODO проверка существования пользователя с данным username

        async with ClientSession() as client:
            error = ""
            response: AuthResponse = None
            is_reader = False
            is_admin = False
            is_librarian = False
            try:
                response = await login_reader(client, serializer.validated_data["username"], serializer.validated_data["password"])
                is_reader = True
            except ClientResponseError as e:
                error = e
            
            if error != "":
                try:
                    response = await login_admin(client, serializer.validated_data["username"], serializer.validated_data["password"])
                    is_admin = True
                except ClientResponseError as e:
                    error = e

                if error != "":
                    try:
                        response = await login_librarian(client, serializer.validated_data["username"], serializer.validated_data["password"])
                        is_librarian = True
                    except ClientResponseError as e:
                        error = e

            if not is_reader and not is_admin and not is_librarian:
                raise Http404("user not found")
            elif is_reader:
                info: UserInfo = await get_login_info(client, response.access_token)
                user_profile = await User.objects.prefetch_related("profile").acreate(
                    username = info.mail,
                    
                )