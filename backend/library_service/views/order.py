from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.exceptions import APIException

from library_service.serializers.order import *

from library_service.models.catalog import Library

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
        if self.action in ["list", "update", "destroy", "get_object"]:
            return OrderSerializer
        elif self.action in ["create"]:
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

        library = Library.objects.get(pk = request["library"])
        order.library = library
        order.save()

        #Обнуляем старый список долгов, которые принесет читатель
        old_borrowed_books = OrderItem.objects.filter(order_to_retun=order).all()

        for order_item in old_borrowed_books:
            order_item.order_to_return = None
            order_item.save()

        exemplars: list[str] = request["books"]

        for exemplar in exemplars:
            OrderItem.objects.create(order = order, exemplar_id = exemplar)

        borrowed_books: list[str] = request["borrowed"] #Здесь список айдишников из Orderitem

        if (borrowed_books.count() > 0):
            for book in borrowed_books:
                order_item = OrderItem.objects.get(pk=book)
                if (order_item is not None):
                    order_item.order_to_return = order
                    order_item.save()

    def get_object(self):
        order_id = self.kwargs["pk"]
        order = self.get_queryset().get(pk=order_id)

        if (order is None):
            raise APIException("order not found", code=404)
        
        return order

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
    
    def get_object(self):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(pk=order_id)
        if (order is None):
            raise APIException("order not found", code=404)
        
        borrowed_books = self.get_queryset().filter(order=order)
        if (borrowed_books.count() == 0):
            raise APIException("borroweds not found", code=404)

        return borrowed_books    