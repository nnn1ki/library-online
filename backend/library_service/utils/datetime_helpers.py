from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from django.utils import timezone


def is_working_hour(dt: datetime) -> bool:
    day = dt.weekday()
    hour = dt.hour

    if settings.DAYS["MONDAY"] <= day <= settings.DAYS["FRIDAY"]:
        return settings.WORKING_HOURS["MONDAY_TO_FRIDAY_START_HOUR"] <= hour < settings.WORKING_HOURS[
            "MONDAY_TO_FRIDAY_END_HOUR"
        ]
    if day == settings.DAYS["SATURDAY"]:
        return settings.WORKING_HOURS["SATURDAY_START_HOUR"] <= hour < settings.WORKING_HOURS["SATURDAY_END_HOUR"]
    return False


def get_notification_now(now: datetime | None = None) -> datetime:
    base_now = now or timezone.now()
    tz_name = getattr(settings, "NOTIFICATION_TIME_ZONE", settings.TIME_ZONE)
    if timezone.is_naive(base_now):
        base_now = timezone.make_aware(base_now, timezone=ZoneInfo(settings.TIME_ZONE))
    return base_now.astimezone(ZoneInfo(tz_name))


def is_holiday(dt: datetime, holidays: list[str] | None = None) -> bool:
    if not holidays:
        return False
    return dt.date().isoformat() in set(holidays)


def is_user_active_recently(user, now: datetime | None = None, active_threshold_hours: float | None = None) -> bool:
    if not user.is_authenticated:
        return False

    profile = getattr(user, "profile", None)
    last_seen = getattr(profile, "last_seen", None)
    if not last_seen:
        return False

    now_aware = now or timezone.now()
    time_since_last_seen = now_aware - last_seen

    if active_threshold_hours is None:
        from library_service.models.library_settings import LibrarySettings

        active_threshold_hours = LibrarySettings.get_settings().staff_notification_active_hours
    active_threshold = timedelta(hours=active_threshold_hours)

    return time_since_last_seen <= active_threshold
