import asyncio
from datetime import datetime, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.utils import timezone

from library_service.emails import send_new_orders_digest_notification, send_order_status_update_notification
from library_service.models.catalog import Library
from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.notifications import get_new_orders_digest_data
from library_service.serializers.staff_order import UpdateOrderSerializer

User = get_user_model()


@pytest.fixture
def library() -> Library:
    return Library.objects.first()


def _create_order_with_new_status(user: User, library: Library, new_time):
    order = Order.objects.create(user=user, library=library)
    new_status = OrderHistory.objects.create(order=order, status=OrderHistory.Status.NEW, description="new")
    OrderHistory.objects.filter(pk=new_status.pk).update(date=new_time)
    return order


@pytest.mark.django_db
def test_get_new_orders_digest_data_classifies_fresh_and_stale(library: Library):
    now = timezone.now()
    reader = User.objects.get(username="user")

    fresh_order = _create_order_with_new_status(reader, library, now - timedelta(minutes=10))
    stale_order = _create_order_with_new_status(reader, library, now - timedelta(hours=2))

    not_new_order = _create_order_with_new_status(reader, library, now - timedelta(minutes=30))
    processing_status = OrderHistory.objects.create(
        order=not_new_order,
        status=OrderHistory.Status.PROCESSING,
        description="processing",
    )
    OrderHistory.objects.filter(pk=processing_status.pk).update(date=now - timedelta(minutes=5))

    fresh_orders, stale_orders, _, _ = get_new_orders_digest_data(window_minutes=60, now=now)

    assert [order.id for order in fresh_orders] == [fresh_order.id]
    assert [order.id for order in stale_orders] == [stale_order.id]


@pytest.mark.django_db
def test_digest_sends_only_to_active_librarians(monkeypatch, settings, library: Library):
    now = timezone.now()
    settings.DEFAULT_FROM_EMAIL = "noreply@example.com"
    settings.NOTIFICATION_ACTIVE_HOURS = 2

    librarian_group, _ = Group.objects.get_or_create(name="Librarian")

    active_librarian = User.objects.create_user(username="active_lib", email="active@example.com", password="1234")
    active_librarian.last_login = now - timedelta(minutes=20)
    active_librarian.save(update_fields=["last_login"])
    active_librarian.groups.add(librarian_group)

    inactive_librarian = User.objects.create_user(username="inactive_lib", email="inactive@example.com", password="1234")
    inactive_librarian.last_login = now - timedelta(hours=5)
    inactive_librarian.save(update_fields=["last_login"])
    inactive_librarian.groups.add(librarian_group)

    reader = User.objects.get(username="user")
    fresh_order = _create_order_with_new_status(reader, library, now - timedelta(minutes=15))

    class FakeEmail:
        sent_to: list[str] = []

        def __init__(self, subject, body, from_email, to):  # pylint: disable=unused-argument
            self.to = to

        def attach_alternative(self, html_body, content_type):  # pylint: disable=unused-argument
            return None

        def send(self, fail_silently=False):  # pylint: disable=unused-argument
            FakeEmail.sent_to.extend(self.to)
            return 1

    monkeypatch.setattr("library_service.emails.EmailMultiAlternatives", FakeEmail)

    asyncio.run(
        send_new_orders_digest_notification(
            fresh_orders=[fresh_order],
            stale_new_orders=[],
            email_mode="test",
            window_minutes=60,
            now=now,
        )
    )

    assert "active@example.com" in FakeEmail.sent_to
    assert "inactive@example.com" not in FakeEmail.sent_to


@pytest.mark.django_db
def test_status_notification_respects_mode_and_working_hours(monkeypatch, settings, library: Library):
    user = User.objects.get(username="user")
    user.email = "reader@example.com"
    user.save(update_fields=["email"])

    order = Order.objects.create(user=user, library=library)
    calls = []

    def fake_send_mail(subject, message, from_email, recipients, fail_silently=False):  # pylint: disable=unused-argument
        calls.append((subject, tuple(recipients)))
        return 1

    monkeypatch.setattr("library_service.emails.send_mail", fake_send_mail)

    settings.NOTIFICATION_TIME_ZONE = "Asia/Irkutsk"
    outside_hours = datetime(2026, 1, 5, 3, 0, tzinfo=ZoneInfo("Asia/Irkutsk"))

    asyncio.run(
        send_order_status_update_notification(
            order,
            OrderHistory.Status.READY,
            "ready",
            email_mode="prod",
            now=outside_hours,
        )
    )
    assert calls == []

    asyncio.run(
        send_order_status_update_notification(
            order,
            OrderHistory.Status.READY,
            "ready",
            email_mode="test",
            now=outside_hours,
        )
    )
    assert len(calls) == 1

    asyncio.run(
        send_order_status_update_notification(
            order,
            OrderHistory.Status.READY,
            "ready",
            email_mode="off",
            now=outside_hours,
        )
    )
    assert len(calls) == 1


@pytest.mark.django_db
def test_update_order_serializer_processing_notifies_only_once(monkeypatch, settings, library: Library):
    settings.EMAIL_MODE = "test"

    staff = User.objects.create_user(username="staff_user", password="1234")
    reader = User.objects.get(username="user")

    order = _create_order_with_new_status(reader, library, timezone.now())

    calls = []

    async def fake_status_notification(order, new_status, description, email_mode):
        calls.append((order.id, new_status, description, email_mode))

    monkeypatch.setattr(
        "library_service.serializers.staff_order.send_order_status_update_notification",
        fake_status_notification,
    )

    serializer = UpdateOrderSerializer(context={"request": SimpleNamespace(user=staff)})

    asyncio.run(
        serializer.aupdate(
            order,
            {
                "status": {"status": OrderHistory.Status.PROCESSING, "description": "start"},
                "books": [],
            },
        )
    )
    asyncio.run(
        serializer.aupdate(
            order,
            {
                "status": {"status": OrderHistory.Status.PROCESSING, "description": "repeat"},
                "books": [],
            },
        )
    )

    assert len(calls) == 1
    assert calls[0][1] == OrderHistory.Status.PROCESSING


@pytest.mark.django_db
def test_update_order_serializer_ready_and_cancelled_paths_notify(monkeypatch, settings, library: Library):
    settings.EMAIL_MODE = "test"

    staff = User.objects.create_user(username="staff_user_2", password="1234")
    reader = User.objects.get(username="user")

    calls = []

    async def fake_status_notification(order, new_status, description, email_mode):
        calls.append((order.id, new_status, description, email_mode))

    monkeypatch.setattr(
        "library_service.serializers.staff_order.send_order_status_update_notification",
        fake_status_notification,
    )

    serializer = UpdateOrderSerializer(context={"request": SimpleNamespace(user=staff)})

    ready_order = _create_order_with_new_status(reader, library, timezone.now())
    OrderItem.objects.create(order=ready_order, book_id="book-ready")

    asyncio.run(
        serializer.aupdate(
            ready_order,
            {
                "status": {"status": OrderHistory.Status.READY, "description": "ready"},
                "books": [],
            },
        )
    )

    auto_cancel_order = _create_order_with_new_status(reader, library, timezone.now())
    auto_cancel_item = OrderItem.objects.create(order=auto_cancel_order, book_id="book-cancel")

    asyncio.run(
        serializer.aupdate(
            auto_cancel_order,
            {
                "status": {"status": OrderHistory.Status.READY, "description": "no books"},
                "books": [
                    {
                        "book_id": str(auto_cancel_item.id),
                        "status": "cancelled",
                        "description": "missing",
                    }
                ],
            },
        )
    )

    explicit_cancel_order = _create_order_with_new_status(reader, library, timezone.now())
    OrderItem.objects.create(order=explicit_cancel_order, book_id="book-explicit")

    asyncio.run(
        serializer.aupdate(
            explicit_cancel_order,
            {
                "status": {"status": OrderHistory.Status.CANCELLED, "description": "manual cancel"},
                "books": [],
            },
        )
    )

    statuses = [call[1] for call in calls]
    assert OrderHistory.Status.READY in statuses
    assert statuses.count(OrderHistory.Status.CANCELLED) == 2


@pytest.mark.django_db
def test_send_new_orders_digest_command_calls_sender_only_with_fresh(monkeypatch, library: Library):
    now = timezone.now()
    reader = User.objects.get(username="user")

    fresh_order = _create_order_with_new_status(reader, library, now - timedelta(minutes=20))
    stale_order = _create_order_with_new_status(reader, library, now - timedelta(hours=4))

    received = {}

    async def fake_sender(fresh_orders, stale_new_orders, email_mode, window_minutes, now=None):
        received["fresh"] = [order.id for order in fresh_orders]
        received["stale"] = [order.id for order in stale_new_orders]
        received["mode"] = email_mode
        received["window"] = window_minutes

    monkeypatch.setattr(
        "library_service.management.commands.send_new_orders_digest.send_new_orders_digest_notification",
        fake_sender,
    )

    call_command("send_new_orders_digest", "--window-minutes", "60", "--email-mode", "test")

    assert received["fresh"] == [fresh_order.id]
    assert received["stale"] == [stale_order.id]
    assert received["mode"] == "test"
    assert received["window"] == 60


@pytest.mark.django_db
def test_send_new_orders_digest_command_skips_without_fresh(monkeypatch, library: Library):
    now = timezone.now()
    reader = User.objects.get(username="user")

    _create_order_with_new_status(reader, library, now - timedelta(hours=3))

    was_called = {"value": False}

    async def fake_sender(*args, **kwargs):  # pylint: disable=unused-argument
        was_called["value"] = True

    monkeypatch.setattr(
        "library_service.management.commands.send_new_orders_digest.send_new_orders_digest_notification",
        fake_sender,
    )

    call_command("send_new_orders_digest", "--window-minutes", "60", "--email-mode", "test")

    assert was_called["value"] is False
