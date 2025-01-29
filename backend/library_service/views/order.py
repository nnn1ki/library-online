from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.exceptions import APIException

from library_service.serializers.order import *

class OrderViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "destroy"]:
            return OrderSerializer
        elif self.action in ["create", "update"]:
            return CreateOrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        order_id = kwargs["pk"]
        order = self.get_queryset().filter(pk=order_id).first()

        if (order is None):
            raise APIException("Order not found", code=404)

        order_statuses = OrderHistory.objects.filter(order=order).all()
        
        #Когда статус new, то в истории статусов заказа будет только одна запись
        if (order_statuses.count() > 1):
            raise APIException("Order status is not new", code=400)
        
        OrderItem.objects.filter(order=order).all().delete()

        
    
    def destroy(self, request, *args, **kwargs):
        order_id = kwargs["pk"]
        order = self.get_queryset().filter(pk=order_id).first()

        if (order is None):
            raise APIException("Order not found", code=404)

        #Список допустимых состояний заказа
        acceptable_statuses = [OrderHistory.Status.NEW, OrderHistory.Status.PROCESSING, OrderHistory.Status.READY]
        #Нам интересно только последний статус заказа
        order_last_status = OrderHistory.objects.filter(order=order).last()        

        if (order_last_status.status not in acceptable_statuses):
            raise APIException("Order status is done or later")
        
        order.delete()
            

class BorrowedViewset (
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, handed=True, returned=False)
    