from library_service.emails import send_order_status_update_notification
from library_service.models.order import Order, OrderHistory


NOTIFIABLE_READER_STATUSES = {
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
    if new_status not in NOTIFIABLE_READER_STATUSES:
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
