from datetime import timedelta

from django.utils import timezone

from library_service.models.user import UserProfile


class UpdateLastSeenMiddleware:
    min_update_interval = timedelta(minutes=5)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return response

        now = timezone.now()
        profile = UserProfile.objects.filter(user_id=user.id).only("id", "last_seen").first()
        if profile is None:
            return response

        if profile.last_seen and now - profile.last_seen < self.min_update_interval:
            return response

        UserProfile.objects.filter(pk=profile.pk).update(last_seen=now)
        return response
