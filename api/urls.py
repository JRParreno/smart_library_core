from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, UploadPhotoView, RequestPasswordResetEmail)

from department.views import DepartmentListView
from book.views import (BookListView, BookSavedListView, BookSavedDeleteView,
                        BookRateView, BookEventsView, BookDetailView, BookSavedCreateView,
                        BookRateListView)

app_name = 'api'


router = DefaultRouter()
router.register('book-rate', BookRateView, basename='book-rates')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

    path('forgot-password', RequestPasswordResetEmail.as_view(),
         name='forgot-password '),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),

    # department
    path('department-list', DepartmentListView.as_view(), name='department-list'),

    # book
    path('book-list', BookListView.as_view(), name='book-list'),
    path('book-detail/<pk>', BookDetailView.as_view(), name='book-detail'),
    path('book-events-view-count', BookEventsView.as_view(),
         name='book-events-view-count'),
    path('book-saved-list', BookSavedListView.as_view(),
         name='book-saved-list'),
    path('book-saved-create', BookSavedCreateView.as_view(),
         name='book-saved-create'),
    path('book-saved-delete/<pk>', BookSavedDeleteView.as_view(),
         name='book-saved-delete'),
    path('book-rate-filter', BookRateListView.as_view(), name='book-rate'),
]

urlpatterns += router.urls
