from django.urls import path
from django.contrib.auth import views as auth_views

from user_profile.views import (ProfileView,
                                RegisterView, ChangePasswordView, UploadPhotoView, RequestPasswordResetEmail)

from department.views import DepartmentListView
from book.views import BookListView

app_name = 'api'

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

]
