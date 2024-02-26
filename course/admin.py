from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdminView(admin.ModelAdmin):
    model = Course
    fields = ('name', 'acronym', 'department')
    search_fields = ('name', 'acronym',)
    list_display = ('name',)
