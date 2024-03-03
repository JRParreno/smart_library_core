from functools import reduce
from operator import or_
from rest_framework import generics, permissions, response, status, filters
from book.custom_search import BookCustomSearchFilter

from .serializers import BookSerializer
from .models import Book
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q, F


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = []
    queryset = Book.objects.all().order_by('-popularity')
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [BookCustomSearchFilter]
