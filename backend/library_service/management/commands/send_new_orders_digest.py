import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand

from library_service.emails import send_new_orders_digest_notification
from library_service.notifications import get_new_orders_digest_data


class Command(BaseCommand):
    help = "Send hourly digest about new orders to active librarians"

    def add_arguments(self, parser):
        parser.add_argument(
            "--window-minutes",
            type=int,
            default=None,
            help="Window in minutes for 'fresh' NEW orders",
        )
        parser.add_argument(
            "--email-mode",
            type=str,
            default=None,
            choices=["prod", "test", "off"],
            help="Email mode override (prod/test/off)",
        )

    def handle(self, *args, **options):
        window_minutes = options["window_minutes"] or getattr(settings, "NOTIFICATION_DIGEST_WINDOW_MINUTES", 60)
        email_mode = (options["email_mode"] or getattr(settings, "EMAIL_MODE", "prod")).lower()

        fresh_orders, stale_new_orders, now_aware, _ = get_new_orders_digest_data(window_minutes=window_minutes)

        if not fresh_orders:
            self.stdout.write(self.style.WARNING("Digest: no fresh NEW orders in current window, skipping."))
            return

        self.stdout.write(
            f"Digest: fresh={len(fresh_orders)}, stale_new={len(stale_new_orders)}, mode={email_mode}, window={window_minutes}m"
        )

        try:
            asyncio.run(
                send_new_orders_digest_notification(
                    fresh_orders=fresh_orders,
                    stale_new_orders=stale_new_orders,
                    email_mode=email_mode,
                    window_minutes=window_minutes,
                    now=now_aware,
                )
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.stderr.write(self.style.ERROR(f"Digest: command failed with error: {exc}"))
            raise
