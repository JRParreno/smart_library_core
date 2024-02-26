from rest_framework import generics, permissions, response, status

from user_profile.models import UserProfile
from .serializers import DepartmentSerializer
from .models import Department
from .paginate import ExtraSmallResultsSetPagination
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes


class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = []
    queryset = Department.objects.all().order_by('name')
    pagination_class = ExtraSmallResultsSetPagination
