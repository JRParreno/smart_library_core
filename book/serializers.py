from rest_framework import serializers

from .models import Book, BookPhotos, Tags, BookRate, BookSaved, BookViewCount
from department.serializers import DepartmentSerializer
from django.db.models import Sum


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['pk', 'name', 'acronym']


class BookSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = Book
        fields = ['pk', 'department', 'title', 'author', 'popularity', 'cover_photo',
                  'description', 'number_copies', 'year',
                  'tags', 'isbn_issn', 'ddc_number', 'edition_statement',
                  'publisher', 'imprint', 'physical_description',
                  'control_number', 'call_number', 'general_information',
                  'discipline'
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
            current_user = self.request.user
            book = data['pk']
            # get book photos
            book_photos = BookPhotos.objects.filter(book__pk=book)
            book_object_photos = []
            for book_photo in book_photos:
                if book_photo.image:
                    book_object_photos.append(
                        self.request.build_absolute_uri(book_photo.image.url))
            data['book_photos'] = book_object_photos
            # get number of total rate

            book_rates = BookRate.objects.filter(
                book__pk=book)
            total_sum = book_rates.aggregate(Sum('rate'))
            total_rate = total_sum['rate__sum'] / book_rates.count()
            user_rate = BookRate.objects.filter(
                user__pk=current_user.pk, book__pk=book)
            save_books = BookSaved.objects.filter(
                book__pk=book, user__pk=current_user.pk)
            view_count = BookViewCount.objects.filter(
                book__pk=book).count()

            data['total_rate'] = total_rate
            data['view_count'] = view_count
            data['is_rate'] = user_rate.exists()
            data['rate_pk'] = user_rate.first(
            ).pk if user_rate.exists() else None
            data['is_save'] = save_books.exists()
            data['save_pk'] = save_books.first(
            ).pk if save_books.exists() else None
            data['rate'] = user_rate.first().rate if user_rate.exists() else 0

        return data


class BookRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookRate
        fields = ['book', 'rate']


class BookSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSaved
        fields = ['pk', 'book']

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(BookSavedSerializer, self).__init__(*args, **kwargs)


class BookSavedListSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookSaved
        fields = ['pk', 'book']

    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(BookSavedListSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        # Access self.request and pass it to the child serializer context
        book_serializer = BookSerializer(
            instance.book, context={'request': self.context.get('request')})
        return book_serializer.data


class BookViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookViewCount
        fields = ['book', 'created_at', 'updated_at']
