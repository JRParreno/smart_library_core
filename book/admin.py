from django.contrib import admin

from .models import Book, BookPhotos, Tags


admin.site.register(Tags)


class ShopPhotoTabularInLine(admin.TabularInline):
    model = BookPhotos
    fields = ('book', 'image')


@admin.register(Book)
class BookAdminView(admin.ModelAdmin):
    model = Book
    search_fields = ('title',)
    list_display = ('title',)
    inlines = [ShopPhotoTabularInLine,]
    filter_horizontal = ['tags',]
