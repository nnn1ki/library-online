from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import requests

from app.local_settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET

from django.contrib.auth.models import User
from django.shortcuts import redirect

class BitrixAuthView(APIView):
    permission_classes = []

    class InnerSerializer(serializers.Serializer):
        code = serializers.CharField()
        state = serializers.CharField(required=False)
        domain = serializers.CharField(required=False)
        member_id = serializers.CharField(required=False)
        scope = serializers.CharField(required=False)
        server_domain = serializers.CharField(required=False)

    def auth_login(user):
        tokens = TokenObtainPairSerializer.get_token(user)
        parse_token = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return Response(status=200, data=parse_token)

    def default_auth_processor(self, state, user):
        self.auth_login(user)
        return redirect("/")

    def get(self, request, *args, **kwargs):
        serializer = self.InnerSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        HTTP_REFERER = request.META.get('HTTP_REFERER') or "/"

        r = requests.get("https://int.istu.edu/oauth/token/?grant_type=authorization_code", {
            "code": serializer.validated_data['code'],
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET,
        }, verify=False)

        response_data = {}

        data = r.json()
        if r.status_code != 200:
            # messages.add_message(request, messages.WARNING, data['error_description'])
            return redirect(HTTP_REFERER)

        data = r.json()
        r = requests.get(data['client_endpoint'] + 'user.info.json', {
            "auth": data['access_token'],
        })
        if r.status_code != 200:
            response_data['result'] = 'Failed'
            response_data['message'] = data['error_description']
            return redirect(HTTP_REFERER)

        data = r.json()
        result = data['result']

        bitrix_user_id = result['id']
        email = result['email']
        user, created = User.objects.get_or_create(
            userprofile__bitrix_user_id=bitrix_user_id,
            defaults={
                "username": email,
                "last_name": result['last_name'] or "",
                "first_name": result['name'] or "",
                "email": result['email'],
            }
        )

        if created:
            user.userprofile.bitrix_user_id = bitrix_user_id
            user.userprofile.save()

        user.userprofile.is_teacher = bool(result['is_teacher'])
        user.userprofile.is_student = bool(result['is_student'])
        user.userprofile.full_name = " ".join(i for i in [result['last_name'], result['name'], result['second_name']] if i)

        mira_id = int(result['mira_id'][0] if result['mira_id'] or 0 else 0)
        if mira_id > 2:
            user.userprofile.mira_id = mira_id

        user.userprofile.save()
        self.auth_login(user)

        return redirect("/")