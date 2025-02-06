from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.mixins import *
from library_service.serializers.order import *

class OrderViewset(
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionCreateModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet
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
    
    async def adestroy(self, request, *args, **kwargs):
        order = await self.aget_object()

        ACCEPTABLE_STATUSES = [OrderHistory.Status.NEW, OrderHistory.Status.PROCESSING, OrderHistory.Status.READY]
        order_last_status = await OrderHistory.objects.filter(order=order).order_by("date").alast() # Нам интересен только последний статус заказа

        if (order_last_status.status not in ACCEPTABLE_STATUSES):
            raise APIException(f"Can't cancel an order with status {order_last_status.status}", code=400)
        
        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.CANCELLED)

        async for book in order.books.all():
            book.status = OrderItem.Status.CANCELLED
            await book.asave()

        return Response(status=status.HTTP_204_NO_CONTENT)

class BorrowedViewset (
    SessionListModelMixin,
    AsyncGenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, status=OrderItem.Status.HANDED)