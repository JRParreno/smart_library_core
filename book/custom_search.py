from rest_framework import filters
from django.db.models import Q, F


class BookCustomSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_fields = request.query_params.get('search_fields')
        departments = request.query_params.get('departments', None)

        if search_fields:
            search_fields = search_fields.split(',')
            or_query = Q()
            for field in search_fields:
                field_value = request.query_params.get(field)
                if field_value:
                    or_query |= Q(**{f'{field}__icontains': field_value})
            queryset = queryset.filter(
                or_query).distinct().order_by('-popularity')

            if departments:
                departments = departments.split(',')
                queryset = queryset.filter(department__id__in=departments)

            if queryset.exists:
                queryset.update(popularity=F('popularity') + 1)
        return queryset
