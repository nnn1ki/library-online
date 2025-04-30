from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

from library_service.opac.api.login import login_reader, login_librarian, login_admin

User = get_user_model()

class AuthViewset(
    AsyncAPIView
):
    async def post(self, request, *args, **kwargs):
        pass