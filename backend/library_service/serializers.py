from rest_framework import serializers

class LibraryNameSerializer(serializers.Serializer):
    library_name = serializers.CharField()

class LibrarySerializer(serializers.Serializer):
    library_name = LibraryNameSerializer()
    description = serializers.CharField()
    address = serializers.CharField()

class BookIdSerializer(serializers.Serializer):
    book_id = serializers.CharField()

class LinkSerializer(serializers.Serializer):
    url = serializers.URLField()
    description = serializers.CharField()

class CopiesSerializer(serializers.Serializer):
    library = LinkSerializer()
    amount = serializers.IntegerField()

class BookSerializer(serializers.Serializer):
    id = BookIdSerializer()
    name = serializers.CharField()
    author = serializers.CharField()
    book_description = serializers.CharField()
    book_logo = serializers.ImageField()
    links = LinkSerializer(many = True)
    library = LibrarySerializer(many = True)
    copies = CopiesSerializer(many = True)
    can_be_ordered = serializers.BooleanField()