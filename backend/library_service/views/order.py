from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from library_service.serializers.order import *

class OrderViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateUpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()

        acceptable_statuses = [OrderHistory.Status.NEW, OrderHistory.Status.PROCESSING, OrderHistory.Status.READY]
        order_last_status = OrderHistory.objects.filter(order=order).order_by("date").last() # Нам интересен только последний статус заказа

        if (order_last_status.status not in acceptable_statuses):
            raise APIException(f"Can't cancel an order with status {order_last_status.status}", code=400)
        
        OrderHistory.objects.create(order=order, status=OrderHistory.Status.CANCELLED)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BorrowedViewset (
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, handed=True, returned=False)
    
    # Если это для retrieve, то можно просто /api/order/{id}/ вызвать
    # def get_object(self):
    #     order_id = self.kwargs["pk"]
    #     order = Order.objects.get(pk=order_id)
    #     if (order is None):
    #         raise APIException("order not found", code=404)
        
    #     borrowed_books = self.get_queryset().filter(order=order)
    #     if (borrowed_books.count() == 0):
    #         raise APIException("borroweds not found", code=404)

    #     return borrowed_books    