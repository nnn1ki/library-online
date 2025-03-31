from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from adrf import mixins as amixins

from library_service.models.library_settings import LibrarySettings
from library_service.serializers.library_settings import LibrarySettingsSerializer


class LibrarySettingsViewSet(amixins.ListModelMixin, AsyncGenericViewSet):
    serializer_class = LibrarySettingsSerializer
    queryset = LibrarySettings.objects.all()

    async def aget_object(self):
        return await LibrarySettings.aget_settings()

    async def alist(self, *args, **kwargs):
        settings: LibrarySettings = await self.aget_object()
        serializer = self.get_serializer(settings)
        return Response(await serializer.adata)

    @action(detail=False, url_path="update", methods=["put"], permission_classes=[IsAuthenticated])  # TODO: IsAdmin
    async def update_settings(self, request, *args, **kwargs):
        serializer = self.get_serializer(await self.aget_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        await serializer.asave()

        return await self.alist(*args, **kwargs)
