from rest_framework import serializers

from library_service.models.catalog import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "description", "address"]

class LinkSerializer(serializers.Serializer):
    url = serializers.URLField()
    description = serializers.CharField()

class BookSerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    cover = serializers.CharField()
    links = LinkSerializer(many = True)
    library = serializers.IntegerField()
    copies = serializers.IntegerField()
    can_be_ordered = serializers.BooleanField()