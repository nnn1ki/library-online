from rest_framework import serializers

# TODO: создать директорию serializers для логического разделения сериалайзеров по файлам (эти сериалайзеры можно поместить в один файл)

class LibrarySerializer(serializers.Serializer):
    library_name = serializers.CharField()
    description = serializers.CharField()
    address = serializers.CharField()

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