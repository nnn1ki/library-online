from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from asgiref.sync import sync_to_async
from django.db.models import OuterRef, Subquery

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.mixins import (
    LockUserMixin,
    SessionCreateModelMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
)

from library_service.models.order import Order, OrderHistory, OrderItem

from library_service.serializers.order import (
    BorrowedBookSerializer,
    CreateUpdateOrderSerializer,
    OrderSerializer,
    UserOrderSerializer,
)

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE
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
        elif self.action in ["new_orders", "processing_orders", "ready_orders", "done_orders"]:
            return UserOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        if self.action in ["new_orders"]:
            return super().get_queryset().prefetch_related("library")
        return super().get_queryset().filter(user=self.request.user).prefetch_related("library")

    @sync_to_async
    def get_data(self, target_status):
        queryset = self.get_queryset()

        last_status_subquery = OrderHistory.objects.filter(order=OuterRef("pk")).order_by("-date").values("status")[:1]

        queryset = queryset.annotate(last_status=Subquery(last_status_subquery)).filter(last_status=target_status)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    # @action(detail=False, methods=["get"], url_path="new")
    # async def new_orders(self, request):
    #     data = await self.get_data(OrderHistory.Status.NEW)
    #     return Response(data)

    # @action(detail=False, methods=["get"], url_path="processing")
    # async def processing_orders(self, request):
    #     data = await self.get_data(OrderHistory.Status.PROCESSING)
    #     return Response(data)

    # @action(detail=False, methods=["get"], url_path="ready")
    # async def ready_orders(self, request):
    #     data = await self.get_data(OrderHistory.Status.READY)
    #     return Response(data)

    # @action(detail=False, methods=["get"], url_path="done")
    # async def done_orders(self, request):
    #     data = await self.get_data("cancelled")
    #     paginator = PageNumberPagination()
    #     paginator.page_size = 5
    #     paginated_queryset = paginator.paginate_queryset(data, request)
    #     return paginator.get_paginated_response(paginated_queryset)

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
