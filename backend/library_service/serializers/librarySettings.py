from rest_framework import serializers
from library_service.models import LibrarySettings

class LibrarySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarySettings
        fields = "__all__"

class CreateUpdateLibrarySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarySettings
        fields = "__all__"
