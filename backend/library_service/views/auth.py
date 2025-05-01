from django.contrib.auth import get_user_model

from adrf.views import APIView as AsyncAPIView

User = get_user_model()


class AuthViewset(AsyncAPIView):
    async def post(self, request, *args, **kwargs):
        pass
