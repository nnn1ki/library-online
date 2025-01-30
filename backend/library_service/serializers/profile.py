from rest_framework import serializers

from library_service.models.user import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ["username", "groups"]
    
    def get_username(self, obj: UserProfile):
        return obj.user.username

    def get_groups(self, obj: UserProfile):
        return [x.name for x in obj.user.groups.all()]