from datetime import datetime, timedelta, timezone as dt_timezone

from django.conf import settings
from django.db.models import DateTimeField, OuterRef, Subquery
from django.utils import timezone

from library_service.models.order import Order, OrderHistory


def get_new_orders_digest_data(
    *, window_minutes: int | None = None, now: datetime | None = None
) -> tuple[list[Order], list[Order], datetime, datetime]:
    """Return fresh and stale orders that currently have NEW status."""
    digest_window_minutes = window_minutes or getattr(settings, "NOTIFICATION_DIGEST_WINDOW_MINUTES", 60)

    now_aware = now or timezone.now()
    if timezone.is_naive(now_aware):
        now_aware = timezone.make_aware(now_aware, timezone=dt_timezone.utc)

    fresh_cutoff = now_aware - timedelta(minutes=digest_window_minutes)

    latest_status_subquery = (
        OrderHistory.objects.filter(order=OuterRef("pk")).order_by("-date").values("status")[:1]
    )
    latest_new_date_subquery = (
        OrderHistory.objects.filter(order=OuterRef("pk"), status=OrderHistory.Status.NEW)
        .order_by("-date")
        .values("date")[:1]
    )

    orders_with_current_new = (
        Order.objects.select_related("user", "library")
        .annotate(current_status=Subquery(latest_status_subquery))
        .annotate(current_new_date=Subquery(latest_new_date_subquery, output_field=DateTimeField()))
        .filter(current_status=OrderHistory.Status.NEW)
        .exclude(current_new_date__isnull=True)
        .order_by("current_new_date", "id")
    )

    fresh_orders: list[Order] = []
    stale_new_orders: list[Order] = []

    for order in orders_with_current_new:
        if order.current_new_date >= fresh_cutoff:
            fresh_orders.append(order)
        else:
            stale_new_orders.append(order)

    return fresh_orders, stale_new_orders, now_aware, fresh_cutoff
