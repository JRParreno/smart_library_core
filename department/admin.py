from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdminView(admin.ModelAdmin):
    model = Department
    fields = ('name', 'acronym')
    search_fields = ('name', 'acronym')
    list_display = ('name',)
