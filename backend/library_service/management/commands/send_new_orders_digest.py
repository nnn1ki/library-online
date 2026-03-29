import asyncio

from django.core.management.base import BaseCommand

from library_service.services.staff_digest import dispatch_staff_digest


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
        try:
            result = asyncio.run(
                dispatch_staff_digest(
                    force=False,
                    email_mode=options["email_mode"],
                )
            )

            if result["reason"] == "interval":
                self.stdout.write(
                    self.style.WARNING("Digest: interval has not elapsed yet, skipping.")
                )
                return

            if result["reason"] == "empty":
                self.stdout.write(self.style.WARNING("Digest: no NEW orders in current window, skipping."))
                return

            self.stdout.write(
                f"Digest: fresh={result['fresh_count']}, stale_new={result['stale_count']}, window={result['window_minutes']}m"
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.stderr.write(self.style.ERROR(f"Digest: command failed with error: {exc}"))
            raise
