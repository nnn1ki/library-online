from rest_framework import serializers

from library_service.models.catalog import *

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "description", "address"]

class LinkSerializer(serializers.Serializer):
    url = serializers.URLField()
    description = serializers.CharField()

class CopiesSerializer(serializers.Serializer):
    library = LinkSerializer()
    amount = serializers.IntegerField()

class BookSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    author = serializers.CharField()
    book_description = serializers.CharField()
    book_logo = serializers.ImageField()
    links = LinkSerializer(many = True)
    copies = CopiesSerializer(many = True)
    can_be_ordered = serializers.BooleanField()