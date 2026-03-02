import asyncio
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string

from library_service.models.order import Order, OrderHistory
from library_service.utils.datetime_helpers import get_notification_now, is_user_active_recently, is_working_hour


def _should_skip_by_schedule(email_mode: str, now: datetime | None = None) -> bool:
    if email_mode.lower() != "prod":
        return False

    current_local_time = get_notification_now(now)
    return not is_working_hour(current_local_time)


def _build_digest_payload(
    fresh_orders: list[Order],
    stale_new_orders: list[Order],
    now: datetime,
    window_minutes: int,
) -> tuple[str, str, str]:
    fresh_count = len(fresh_orders)

    subject = f"Новые заказы за последние {window_minutes} минут: {fresh_count}"

    plain_lines: list[str] = [
        "Здравствуйте, [LIBRARIAN_NAME].",
        "",
        f"За последние {window_minutes} минут поступило новых заказов: {fresh_count}.",
        "",
        f"Новые заказы за последние {window_minutes} минут:",
    ]

    for order in fresh_orders:
        created_at = getattr(order, "first_new_date", None)
        created_at_text = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "N/A"
        plain_lines.append(
            f"- Заказ #{order.id}, читатель: {order.user.email}, библиотека: {order.library.description}, создан: {created_at_text}"
        )

    plain_lines.append("")
    plain_lines.append("Старые заказы со статусом NEW:")

    if stale_new_orders:
        for order in stale_new_orders:
            created_at = getattr(order, "first_new_date", None)
            created_at_text = created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else "N/A"
            plain_lines.append(
                f"- Заказ #{order.id}, читатель: {order.user.email}, библиотека: {order.library.description}, создан: {created_at_text}"
            )
    else:
        plain_lines.append("- Нет")

    plain_lines.append("")
    plain_lines.append("Пожалуйста, проверьте заказы в системе.")

    html_context = {
        "fresh_orders": fresh_orders,
        "stale_orders": stale_new_orders,
        "total_fresh_orders": fresh_count,
        "window_minutes": window_minutes,
        "generated_at": now,
    }
    html_body = render_to_string("emails/new_orders_digest.html", html_context)

    return subject, "\n".join(plain_lines), html_body


async def send_new_orders_digest_notification(
    fresh_orders: list[Order],
    stale_new_orders: list[Order],
    email_mode: str = "prod",
    window_minutes: int = 60,
    now: datetime | None = None,
) -> None:
    email_mode = email_mode.lower()

    if not fresh_orders:
        print("Email digest: no fresh orders, nothing to send.")
        return

    if _should_skip_by_schedule(email_mode, now=now):
        print("Email digest: outside working hours in prod mode, skipping.")
        return

    try:
        librarian_group = await Group.objects.aget(name="Librarian")
    except Group.DoesNotExist:
        print("Email digest: Librarian group not found.")
        return

    librarians_qs = (
        get_user_model()
        .objects.filter(groups=librarian_group)
        .exclude(email__isnull=True)
        .exclude(email="")
        .distinct()
    )
    librarians = [librarian async for librarian in librarians_qs]

    if not librarians:
        print("Email digest: no librarians with email found.")
        return

    generated_at = get_notification_now(now)
    subject, plain_body, html_body = _build_digest_payload(
        fresh_orders,
        stale_new_orders,
        generated_at,
        window_minutes,
    )

    for librarian in librarians:
        if not is_user_active_recently(librarian):
            print(f"Email digest: skip {librarian.username}, not active recently.")
            continue

        body = plain_body.replace("[LIBRARIAN_NAME]", librarian.get_full_name() or librarian.username)

        if email_mode == "off":
            print("--- Console Email (Digest) ---")
            print(f"To: {librarian.email}")
            print(f"Subject: {subject}")
            print(f"Body:\n{body}")
            print("------------------------------")
            continue

        try:
            await asyncio.to_thread(
                send_mail,
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [librarian.email],
                False,
                html_message=html_body,
            )
            print(f"Email digest: sent to {librarian.email}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(f"Email digest: failed for {librarian.email}: {exc}")


async def send_order_status_update_notification(
    order: Order,
    new_status: str,
    description: str,
    email_mode: str = "prod",
    now: datetime | None = None,
) -> None:
    email_mode = email_mode.lower()

    if _should_skip_by_schedule(email_mode, now=now):
        print(f"Status email: outside working hours in prod mode for order #{order.id}, skipping.")
        return

    user = order.user
    if not user.email:
        print(f"Status email: user {user.username} has no email, skipping.")
        return

    subject_map = {
        OrderHistory.Status.PROCESSING: f"Ваш заказ #{order.id} в работе",
        OrderHistory.Status.READY: f"Ваш заказ #{order.id} готов к выдаче",
        OrderHistory.Status.CANCELLED: f"Ваш заказ #{order.id} отменен",
    }
    body_map = {
        OrderHistory.Status.PROCESSING: "Ваш заказ был взят в работу.",
        OrderHistory.Status.READY: "Ваш заказ готов к выдаче.",
        OrderHistory.Status.CANCELLED: "Ваш заказ был отменен.",
    }

    subject = subject_map.get(new_status)
    body_intro = body_map.get(new_status)

    if not subject or not body_intro:
        print(f"Status email: status {new_status} is not configured for notifications.")
        return

    plain_message = f"Здравствуйте, {user.get_full_name() or user.username}.\n\n"
    plain_message += f"{body_intro}\n"
    if description:
        plain_message += f"Комментарий от сотрудника: {description}\n\n"
    plain_message += "Спасибо!"

    if email_mode == "off":
        print("--- Console Email (Status Update) ---")
        print(f"To: {user.email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{plain_message}")
        print("------------------------------------")
        return

    try:
        await asyncio.to_thread(
            send_mail,
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            False,
        )
        print(f"Status email: sent to {user.email} for order #{order.id}")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Status email: failed for {user.email}: {exc}")
