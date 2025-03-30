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

from library_service.serializers.staff_order import (
    UserOrderSerializer,
    OrderSerializer,
)

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE
]

class StaffOrderViewset(
    LockUserMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionCreateModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    #permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["get_orders", "new_orders"]:
            return UserOrderSerializer
        else: 
            return OrderSerializer
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")
    
    @sync_to_async
    def get_data(self, target_status):
        queryset = self.get_queryset()

        last_status_subquery = OrderHistory.objects.filter(order=OuterRef("pk")).order_by("-date").values("status")[:1]

        queryset = queryset.annotate(last_status=Subquery(last_status_subquery)).filter(last_status=target_status)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @action(detail=False, methods=["get"], url_path="order")
    async def get_orders(self, request):
        status = self.request.query_params.get('status')
        target_status = OrderHistory.Status.NEW

        if (status == 'processing'):
            target_status = OrderHistory.Status.PROCESSING
        elif (status == 'ready'):
            target_status = OrderHistory.Status.READY
        elif (status == 'done'):
            target_status = OrderHistory.Status.DONE

        data = await self.get_data(target_status)
        return Response(data)