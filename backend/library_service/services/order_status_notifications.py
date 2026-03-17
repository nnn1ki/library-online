from library_service.models.library_settings import LibrarySettings
from library_service.emails import send_order_status_update_notification
from library_service.models.order import Order, OrderHistory


DEFAULT_NOTIFIABLE_READER_STATUSES = {
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.CANCELLED,
}


async def notify_reader_about_order_status_change(
    *,
    order_id: int,
    new_status: str,
    description: str,
    email_mode: str,
) -> None:
    library_settings = await LibrarySettings.aget_settings()
    if not library_settings.reader_status_notifications_enabled:
        return

    configured_statuses = set(library_settings.reader_notification_statuses or DEFAULT_NOTIFIABLE_READER_STATUSES)
    if new_status not in configured_statuses:
        return

    if new_status == OrderHistory.Status.PROCESSING:
        processing_count = await OrderHistory.objects.filter(
            order_id=order_id,
            status=OrderHistory.Status.PROCESSING,
        ).acount()
        if processing_count > 1:
            return

    order = await Order.objects.select_related("user").aget(pk=order_id)
    await send_order_status_update_notification(order, new_status, description, email_mode)
