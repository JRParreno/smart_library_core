from rest_framework import generics, permissions, response, status
from django_filters import rest_framework as filters

from .serializers import BookSerializer
from .models import Book
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = []
    queryset = Book.objects.all().order_by('-popularity')
    pagination_class = ExtraSmallResultsSetPagination
    # filter_backends = (filters.DjangoFilterBackend,)

    # def get_queryset(self):
    #     tags = self.request.query_params.getlist('tags', None)
    #     print(tags)
    #     return Book.objects.filter(tags__acronym__in=tags).order_by('-popularity')
