from rest_framework import serializers

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.user import UserProfile


class ProfileSerializer(aserializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    groups = afields.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["username", "groups", "first_name", "last_name"]

    def get_username(self, obj: UserProfile):
        return obj.user.username

    def get_first_name(self, obj: UserProfile):
        return obj.user.first_name

    def get_last_name(self, obj: UserProfile):
        return obj.user.last_name

    async def get_groups(self, obj: UserProfile):
        return [x.name async for x in obj.user.groups.all()]
