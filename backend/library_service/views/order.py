from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from library_service.serializers.order import *

class OrderViewset(
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class BorrowedViewset (
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, handed=True, returned=False)
    