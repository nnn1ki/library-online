from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.conf import settings
from django.utils import timezone

WEEKDAY_KEYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)

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


def _time_to_minutes(value: str) -> int:
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def get_effective_staff_schedule_window(
    dt: datetime,
    week_schedule: dict | None = None,
    schedule_overrides: dict | None = None,
    holidays: list[str] | None = None,
) -> dict | None:
    if is_holiday(dt, holidays):
        return None

    date_key = dt.date().isoformat()
    override = (schedule_overrides or {}).get(date_key)
    if isinstance(override, dict):
        return override if override.get("enabled") else None

    day_key = WEEKDAY_KEYS[dt.weekday()]
    day_schedule = (week_schedule or {}).get(day_key)
    if not isinstance(day_schedule, dict):
        return None

    return day_schedule if day_schedule.get("enabled") else None


def is_within_staff_schedule(
    dt: datetime,
    week_schedule: dict | None = None,
    schedule_overrides: dict | None = None,
    holidays: list[str] | None = None,
) -> bool:
    schedule_window = get_effective_staff_schedule_window(
        dt,
        week_schedule=week_schedule,
        schedule_overrides=schedule_overrides,
        holidays=holidays,
    )
    if not schedule_window:
        return False

    current_minutes = dt.hour * 60 + dt.minute
    start_minutes = _time_to_minutes(schedule_window["start"])
    end_minutes = _time_to_minutes(schedule_window["end"])
    return start_minutes <= current_minutes < end_minutes


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
