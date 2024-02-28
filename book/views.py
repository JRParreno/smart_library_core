from functools import reduce
from operator import or_
from rest_framework import generics, permissions, response, status, filters
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BookSerializer
from .models import Book
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = []
    queryset = Book.objects.all().order_by('-popularity')
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        tags = self.request.query_params.get('tags', None)
        if tags:
            myTags = tags.split(',')
            q_object = reduce(or_, (Q(tags__acronym__icontains=tag)
                              for tag in myTags))
            return Book.objects.filter(q_object).order_by('-popularity').distinct()
        return super().get_queryset()
