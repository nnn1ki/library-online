from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.models import User, Group

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

class BitrixAuthView(AsyncAPIView):
    class Serializer(serializers.Serializer):
        code = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:
            token_response = await client.get("https://int.istu.edu/oauth/token/?grant_type=authorization_code", params={
                "code": serializer.validated_data["code"],
                "client_id": settings.OAUTH_CLIENT_ID,
                "client_secret": settings.OAUTH_CLIENT_SECRET,
            })

            token_response_data = await token_response.json()
            if token_response.status != 200:
                raise AuthenticationFailed(token_response_data["error_description"], code="token_response")

            userinfo_response = await client.get(token_response_data["client_endpoint"] + "user.info.json", params={
                "auth": token_response_data["access_token"],
            })

            userinfo_response_data = await userinfo_response.json()
            if userinfo_response.status != 200:
                raise AuthenticationFailed(userinfo_response_data["error_description"], code="userinfo_response")

            result = userinfo_response_data["result"]

            campus_id = result["id"]
            email = result["email"]
            user, created = await User.objects.prefetch_related("profile").aget_or_create(
                profile__campus_id=campus_id,
                defaults={
                    "username": email,
                    "email": email,
                    "first_name": result["name"] or "",
                    "last_name": result["last_name"] or ""
                }
            )

            if created:
                await user.groups.aadd(await Group.objects.aget(name="Reader"))
                user.profile.campus_id = campus_id
                await user.asave()

            # user.profile.is_teacher = bool(result["is_teacher"])
            # user.profile.is_student = bool(result["is_student"])
            # user.profile.full_name = " ".join(i for i in [result["last_name"], result["name"], result["second_name"]] if i)

            mira_id = int(result["mira_id"][0] if result["mira_id"] or 0 else 0)
            if mira_id > 2:
                user.profile.mira_id = mira_id

            await user.profile.asave()

            # TODO: это можно в асинке переписать
            tokens = await sync_to_async(TokenObtainPairSerializer.get_token)(user)
            return Response(status=200, data={
                "refresh": str(tokens),
                "access": str(tokens.access_token)
            })