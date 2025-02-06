from aiohttp import ClientSession
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.serializers.order import *

class OrderViewset(
    amixins.ListModelMixin,
    amixins.RetrieveModelMixin,
    amixins.CreateModelMixin,
    amixins.UpdateModelMixin,
    AsyncGenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    client_session: ClientSession | None = None

    def get_serializer_class(self):
        if self.action in ["acreate", "aupdate"]:
            return CreateUpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).prefetch_related("library")
    
    # TODO: можно вынести в миксины
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["client_session"] = self.client_session
        return context
    
    async def alist(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().alist(*args, **kwargs)
    
    async def aretrieve(self, request, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().aretrieve(request, *args, **kwargs)
    
    async def acreate(self, request, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().acreate(request, *args, **kwargs)
    
    async def aupdate(self, request, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().aupdate(request, *args, **kwargs)
    
    async def adestroy(self, request, *args, **kwargs):
        order = await self.aget_object()

        ACCEPTABLE_STATUSES = [OrderHistory.Status.NEW, OrderHistory.Status.PROCESSING, OrderHistory.Status.READY]
        order_last_status = await OrderHistory.objects.filter(order=order).order_by("date").alast() # Нам интересен только последний статус заказа

        if (order_last_status.status not in ACCEPTABLE_STATUSES):
            raise APIException(f"Can't cancel an order with status {order_last_status.status}", code=400)
        
        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.CANCELLED)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BorrowedViewset (
    amixins.ListModelMixin,
    AsyncGenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, handed=True, returned=False)