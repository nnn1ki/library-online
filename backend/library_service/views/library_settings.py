from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.exceptions import APIException


from library_service.models.library_settings import LibrarySettings
from library_service.serializers.library_settings import LibrarySettingsSerializer, CreateUpdateLibrarySettingsSerializer

class LibrarySettingsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = LibrarySettings.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateUpdateLibrarySettingsSerializer
        return LibrarySettingsSerializer

    def get_queryset(self):
        """Фильтрация данных для пользователя (например, администратор библиотеки может видеть только свои настройки)."""
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        """Блокировка удаления настроек библиотеки."""
        raise APIException("Удаление настроек библиотеки запрещено", code=400)
