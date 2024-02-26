from rest_framework import serializers

from .models import Book, BookPhotos, Tags
from department.serializers import DepartmentSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['pk', 'name', 'acronym']


class BookSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = Book
        fields = ['pk', 'department', 'title', 'popularity', 'cover_photo',
                  'description', 'number_copies', 'view_count', 'year', 'author',
                  'tags',
                  ]

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(BookSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        data = super(BookSerializer,
                     self).to_representation(instance)

        if 'request' in self.context and self.request:
            book = data['pk']
            book_photos = BookPhotos.objects.filter(book__pk=book)
            book_object_photos = []
            for book_photo in book_photos:
                if book_photo.image:
                    book_object_photos.append(
                        self.request.build_absolute_uri(book_photo.image.url))
            data['book_photos'] = book_object_photos
        return data
