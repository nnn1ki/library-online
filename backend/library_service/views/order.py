from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from asgiref.sync import sync_to_async
from django.db.models import OuterRef, Subquery

from django.contrib.auth.hashers import make_password

from django.contrib.auth import get_user_model

User = get_user_model()

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
]


class OrderViewset(
    LockUserMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionCreateModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["acreate", "aupdate"]:
            return CreateUpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")
    
    @sync_to_async
    def get_data(self, user):
        queryset = self.get_queryset()

        queryset = queryset.filter(user = user)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @action(detail=False, methods=["get"], url_path="current")
    async def get_orders(self, request):
        username = self.request.query_params.get('user')
        
        if await User.objects.filter(username = username).aexists():
            user = await User.objects.aget(username = username)
        else:
            user = await User.objects.acreate(
                username = username,
                password = make_password('1234'),
                is_active = True
            )

        data = await self.get_data(user)
        print(data)
        return Response(data)

    async def acreate(self, *args, **kwargs):
        return await super().acreate(*args, **kwargs)

#    @LockUserMixin.lock_request
    async def aupdate(self, *args, **kwargs):
        return await super().aupdate(*args, **kwargs)

#    @LockUserMixin.lock_request
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
