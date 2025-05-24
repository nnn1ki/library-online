from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.mixins import (
    LockUserMixin,
    SessionCreateModelMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
)

from library_service.models.order import Order, OrderHistory, OrderItem

from library_service.serializers.order import BorrowedBookSerializer, CreateUpdateOrderSerializer, OrderSerializer

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE,
]


class OrderViewset(
    LockUserMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionCreateModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["acreate", "aupdate"]:
            return CreateUpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).prefetch_related("library")

    @LockUserMixin.lock_request
    async def acreate(self, *args, **kwargs):
        return await super().acreate(*args, **kwargs)

    @LockUserMixin.lock_request
    async def aupdate(self, *args, **kwargs):
        return await super().aupdate(*args, **kwargs)

    @LockUserMixin.lock_request
    async def adestroy(self, request, *args, **kwargs):
        order = await self.aget_object()

        order_last_status = (
            await OrderHistory.objects.filter(order=order).order_by("date").alast()
        )  # Нам интересен только последний статус заказа

        if order_last_status.status not in ACCEPTABLE_STATUSES:
            raise ValidationError(
                f"Can't cancel an order with status {order_last_status.status}",
                code="cant_cancel_order",
            )

        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.CANCELLED)

        async for book in order.books.all():
            book.status = OrderItem.Status.CANCELLED
            await book.asave()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowedViewset(SessionListModelMixin, AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, status=OrderItem.Status.HANDED)
