from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from asgiref.sync import sync_to_async
from django.db.models import OuterRef, Subquery

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.models.user import UserProfile

from library_service.opac.api.ticket import opac_reader_loans
from library_service.opac.book import book_retrieve_by_id

from aiohttp import ClientSession

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
    UpdateOrderSerializer,
    BorrowedBookSerializer,
    CheckOrderSerializer,
)

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE
]

class StaffOrderViewset(
    SessionListModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["get_orders"]:
            return UserOrderSerializer
        elif self.action in ["update_order"]:
            return UpdateOrderSerializer
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

        if (status == 'new'):
            target_status = OrderHistory.Status.NEW
        elif (status == 'processing'):
            target_status = OrderHistory.Status.PROCESSING
        elif (status == 'ready'):
            target_status = OrderHistory.Status.READY
        else:
            target_status = OrderHistory.Status.DONE

        data = await self.get_data(target_status)
        return Response(data)
    
class StaffOrderGetUpdateViewset(
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    #permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action in ["aupdate"]:
            return UpdateOrderSerializer
        elif self.action in ["check_order"]:
            return CheckOrderSerializer
        else: 
            return OrderSerializer
        
    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")
    
    @sync_to_async
    def get_order_and_profile(self, order_id):
        order: Order = self.get_queryset().filter(id=order_id).first()
        profile: UserProfile = UserProfile.objects.get(user = order.user)
        return order, profile
    
    @action(detail=False, methods=["GET"], url_path="check/(?P<order_id>\w+)")
    async def check_order(self, request, order_id = None):      
        order, profile = await self.get_order_and_profile(order_id)

        loans_id_list = []

        async with ClientSession() as client:
            loans = await opac_reader_loans(client, profile.library_card)

            for loan in loans:
                book = await book_retrieve_by_id(client, loan.db, loan.book)
                loans_id_list.append(book.id)  

        serializer = self.get_serializer(order, loans_id_list)
        print(serializer.is_valid())
        return Response(await serializer.adata)

        
class StaffBorrowedViewset(
    SessionRetrieveModelMixin,
    SessionListModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = BorrowedBookSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")

    #Получаем спсиок задолжностей, которые обещали принести с заказом
    async def aget_object(self):
        pk = self.kwargs["pk"]
        order: Order = await self.get_queryset().filter(id=pk).afirst()

        return await self.get_queryset().filter(order_to_return = order)
