from aiohttp import ClientSession
from threading import Lock
from adrf import mixins as amixins
from rest_framework.exceptions import PermissionDenied


# Довольно костыльное решение, чтобы избежать случаев, когда два запроса одновременно обращаются к БД (data races)
# Лучше вместо этого использовать транзакции - @transaction.atomic
# Но транзакции еще не поддерживаются в асинк коде 😢, так что пока используем такое решение
class LockUserMixin:
    mutex = Lock()
    current_users: set[str] = set()

    @staticmethod
    def lock_request(request_handler):
        async def handler(self, *args, **kwargs):
            try:
                self.lock_user()
                return await request_handler(self, *args, **kwargs)
            finally:
                self.unlock_user()

        return handler

    def lock_user(self):
        cls = self.__class__
        username = self.request.user.username
        with cls.mutex:
            if username in cls.current_users:
                raise PermissionDenied("A request is already being processed", code="no_transactions??")
            else:
                cls.current_users.add(username)

    def unlock_user(self):
        cls = self.__class__
        cls.current_users.discard(self.request.user.username)


class ClientSessionMixin:
    client_session: ClientSession | None = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["client_session"] = self.client_session
        return context


class SessionListModelMixin(ClientSessionMixin, amixins.ListModelMixin):
    async def alist(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().alist(*args, **kwargs)


class SessionRetrieveModelMixin(ClientSessionMixin, amixins.RetrieveModelMixin):
    async def aretrieve(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().aretrieve(*args, **kwargs)


class SessionCreateModelMixin(ClientSessionMixin, amixins.CreateModelMixin):
    async def acreate(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().acreate(*args, **kwargs)


class SessionUpdateModelMixin(ClientSessionMixin, amixins.UpdateModelMixin):
    async def aupdate(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().aupdate(*args, **kwargs)


class SessionDestroyModelMixin(ClientSessionMixin, amixins.DestroyModelMixin):
    async def adestroy(self, *args, **kwargs):
        async with ClientSession() as client:
            self.client_session = client
            return await super().adestroy(*args, **kwargs)
