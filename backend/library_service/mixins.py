from aiohttp import ClientSession
from adrf import mixins as amixins

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