from django.contrib import admin

from .models import Book, BookPhotos, Tags, BookRate, BookSaved, BookViewCount


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


@admin.register(BookRate)
class BookRateAdminView(admin.ModelAdmin):
    model = BookRate
    search_fields = ('book__title',)
    list_filter = ['rate',]


@admin.register(BookSaved)
class BookSavedAdminView(admin.ModelAdmin):
    model = BookSaved
    search_fields = ('book__title',)


@admin.register(BookViewCount)
class BookViewCountAdminView(admin.ModelAdmin):
    model = BookViewCount
    search_fields = ('book__title',)
