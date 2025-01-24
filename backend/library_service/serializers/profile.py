from rest_framework import serializers

from library_service.models.user import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(source="user", slug_field="username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["username"]