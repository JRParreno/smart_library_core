from django.contrib import admin

from book.export import export_as_csv

from .models import Book, BookPhotos, Tags, BookRate, BookSaved, BookViewCount


admin.site.register(Tags)


class ShopPhotoTabularInLine(admin.TabularInline):
    model = BookPhotos
    fields = ('book', 'image')


@admin.register(Book)
class BookAdminView(admin.ModelAdmin):
    actions = [export_as_csv]
    model = Book
    readonly_fields = ['rate', 'popularity']
    search_fields = ('title',)
    list_display = ('title', 'author', 'publisher', 'popularity', 'rate')
    inlines = [ShopPhotoTabularInLine,]
    filter_horizontal = ['tags',]


# @admin.register(BookRate)
# class BookRateAdminView(admin.ModelAdmin):
#     model = BookRate
#     search_fields = ('book__title',)
#     list_filter = ['rate',]


@admin.register(BookSaved)
class BookSavedAdminView(admin.ModelAdmin):
    model = BookSaved
    search_fields = ('book__title',)
    list_display = ('user', 'book',)


# @admin.register(BookViewCount)
# class BookViewCountAdminView(admin.ModelAdmin):
#     model = BookViewCount
#     search_fields = ('book__title',)
