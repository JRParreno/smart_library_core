from functools import reduce
from operator import or_
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status, filters, viewsets
from book.custom_search import BookCustomSearchFilter

from .serializers import BookSerializer, BookRateSerializer, BookSavedSerializer, BookViewCountSerializer, BookSavedListSerializer
from .models import Book, BookRate, BookSaved, BookViewCount
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q, F


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = []
    queryset = Book.objects.all().order_by('-popularity')
    pagination_class = ExtraSmallResultsSetPagination
    filter_backends = [BookCustomSearchFilter]


class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    permission_classes = []
    queryset = Book.objects.all().order_by('-popularity')


class BookEventsView(generics.CreateAPIView):
    serializer_class = BookViewCountSerializer
    permission_classes = []
    queryset = BookViewCount.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = BookViewCountSerializer(data=request.data)

        if not serializer.is_valid():
            error = {
                "error_message": "Something went wrong"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        book = serializer.validated_data['book']

        if self.request.user.is_anonymous:
            error = {
                "error_message": "User is anonymouse"
            }
            return response.Response(error, status=status.HTTP_200_OK)

        is_exists = BookViewCount.objects.filter(
            user=self.request.user, book__pk=book.pk).exists()
        if is_exists:
            error = {
                "error_message": "Already added in view count events"
            }
            return response.Response(error, status=status.HTTP_200_OK)

        serializer.validated_data['user'] = self.request.user
        serializer.save()
        message = {
            "success_message": "Added new view count for this user"
        }
        return response.Response(message, status=status.HTTP_201_CREATED)


class BookRateView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookRateSerializer
    queryset = BookRate.objects.all()

    def list(self, request):
        queryset = self.queryset
        serializer = BookRateSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            error = {
                "error_message": "Something went wrong"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        book = serializer.validated_data['book']
        user_exists = BookRate.objects.filter(
            user__pk=user.pk, book__pk=book.pk).exists()

        if user_exists:
            error = {
                "error_message": "You already rate this book."
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data['user'] = self.request.user
        serializer.save()

        message = {
            "success_message": "You rate this book!"
        }
        return response.Response(message, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        book_rates = get_object_or_404(queryset, pk=pk)
        serializer = BookRateSerializer(book_rates)
        return response.Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def destroy(self, request, pk=None):
        pass


class BookSavedCreateView(generics.CreateAPIView):
    serializer_class = BookSavedSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookSaved.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error = {
                "error_message": "Something went wrong"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data['user'] = self.request.user

        message = {
            "success_message": "You add this book!"
        }
        serializer.save()
        return response.Response(message, status=status.HTTP_201_CREATED)


class BookSavedListView(generics.ListAPIView):
    serializer_class = BookSavedListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookSaved.objects.all()
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return BookSaved.objects.filter(user__pk=user.pk)


class BookSavedDeleteView(generics.DestroyAPIView):
    serializer_class = BookSavedSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookSaved.objects.all()

    def delete(self, request, pk=None):
        try:
            queryset = self.queryset
            instance = get_object_or_404(queryset, pk=pk)
            instance.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except BookSaved.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
