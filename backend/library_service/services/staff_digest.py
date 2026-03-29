from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async

from library_service.emails import send_new_orders_digest_notification
from library_service.models.library_settings import LibrarySettings
from library_service.notifications import get_new_orders_digest_data


async def dispatch_staff_digest(
    *,
    force: bool = False,
    email_mode: str | None = None,
    now: datetime | None = None,
) -> dict:
    library_settings = await LibrarySettings.aget_settings()
    effective_email_mode = (email_mode or getattr(settings, "EMAIL_MODE", "prod")).lower()
    current_time = now or timezone.now()
    window_minutes = max(1, int(library_settings.staff_digest_stale_order_hours * 60))

    if (
        not force
        and effective_email_mode == "prod"
        and library_settings.staff_digest_last_sent_at
    ):
        next_allowed_run = library_settings.staff_digest_last_sent_at + timedelta(minutes=window_minutes)
        if current_time < next_allowed_run:
            return {
                "sent": False,
                "reason": "interval",
                "window_minutes": window_minutes,
                "fresh_count": 0,
                "stale_count": 0,
            }

    fresh_orders, stale_new_orders, current_time, _ = await sync_to_async(
        get_new_orders_digest_data,
        thread_sensitive=True,
    )(
        window_minutes=window_minutes,
        now=current_time,
    )

    if not fresh_orders and not stale_new_orders:
        return {
            "sent": False,
            "reason": "empty",
            "window_minutes": window_minutes,
            "fresh_count": 0,
            "stale_count": 0,
        }

    sent_any = await send_new_orders_digest_notification(
        fresh_orders=fresh_orders,
        stale_new_orders=stale_new_orders,
        email_mode=effective_email_mode,
        window_minutes=window_minutes,
        now=current_time,
        ignore_schedule=force,
        ignore_disabled=force,
    )

    if sent_any and effective_email_mode == "prod":
        library_settings.staff_digest_last_sent_at = current_time
        await library_settings.asave(update_fields=["staff_digest_last_sent_at"])

    return {
        "sent": sent_any,
        "reason": "sent" if sent_any else "recipients",
        "window_minutes": window_minutes,
        "fresh_count": len(fresh_orders),
        "stale_count": len(stale_new_orders),
    }
