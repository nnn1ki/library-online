from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.conf import settings
from django.contrib.auth.models import User, Group

import requests

class BitrixAuthView(APIView):
    class Serializer(serializers.Serializer):
        code = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        # TODO: заменить на aiohttp и полностью избавить проект от requests
        token_response = requests.get("https://int.istu.edu/oauth/token/?grant_type=authorization_code", {
            "code": serializer.validated_data["code"],
            "client_id": settings.OAUTH_CLIENT_ID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
        }, verify=False)

        token_response_data = token_response.json()
        if (token_response.status_code != 200):
            raise APIException(token_response_data["error_description"], code=401)

        userinfo_response = requests.get(token_response_data["client_endpoint"] + "user.info.json", {
            "auth": token_response_data["access_token"],
        })

        userinfo_response_data = userinfo_response.json()
        if (userinfo_response.status_code != 200):
            raise APIException(userinfo_response_data["error_description"], code=401)

        result = userinfo_response_data["result"]

        campus_id = result["id"]
        email = result["email"]
        user, created = User.objects.get_or_create(
            profile__campus_id=campus_id,
            defaults={
                "username": email,
                "email": email,
                "first_name": result["name"] or "",
                "last_name": result["last_name"] or ""
            }
        )

        if created:
            user.groups.add(Group.objects.get(name="Reader"))
            user.profile.campus_id = campus_id
            user.save()

        # user.profile.is_teacher = bool(result["is_teacher"])
        # user.profile.is_student = bool(result["is_student"])
        # user.profile.full_name = " ".join(i for i in [result["last_name"], result["name"], result["second_name"]] if i)

        mira_id = int(result["mira_id"][0] if result["mira_id"] or 0 else 0)
        if mira_id > 2:
            user.profile.mira_id = mira_id

        user.profile.save()

        tokens = TokenObtainPairSerializer.get_token(user)
        return Response(status=200, data={
            "refresh": str(tokens),
            "access": str(tokens.access_token)
        })