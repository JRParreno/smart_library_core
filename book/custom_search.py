from rest_framework import filters
from django.db.models import Q, F
from .models import BookRate


class BookCustomSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_fields = request.query_params.get('search_fields')
        departments = request.query_params.get('departments', None)
        rate = request.query_params.get('rate', None)
        semesters = request.query_params.get('semesters', None)
        year_levels = request.query_params.get('year_levels', None)

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

            if semesters:
                semesters = semesters.split(',')
                queryset = queryset.filter(semester__in=semesters)

            if year_levels:
                year_levels = year_levels.split(',')
                queryset = queryset.filter(year_level__in=year_levels)

            if rate:
                rateToNum = float(rate)
                queryset = queryset.filter(rate__range=(0, rateToNum))

            if queryset.exists:
                queryset.update(popularity=F('popularity') + 1)
        return queryset
