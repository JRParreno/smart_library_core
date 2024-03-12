import datetime
from django.db import models
from department.models import Department
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Tags(models.Model):
    name = models.CharField(max_length=250)
    acronym = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.acronym + " " + self.name


class Book(models.Model):
    department = models.ForeignKey(
        Department, related_name='department_books', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, default='')
    cover_photo = models.ImageField(
        upload_to='images/books/', blank=True, null=True)
    popularity = models.IntegerField(default=0)
    description = models.TextField(default='')
    number_copies = models.IntegerField(default=0)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    tags = models.ManyToManyField(Tags, blank=True)
    isbn_issn = models.CharField("ISBN/ISSN", max_length=50)
    ddc_number = models.CharField("DDC No.", max_length=50)
    edition_statement = models.CharField("Edition Statement", max_length=250)
    publisher = models.CharField(max_length=80)
    physical_description = models.TextField(
        "Physical Description")
    general_information = models.TextField("General Information", default='')
    discipline = models.CharField(max_length=80, null=True, blank=True)
    imprint = models.CharField(max_length=50, null=True, blank=True)
    control_number = models.CharField(
        "Control No.", max_length=50, null=True, blank=True)
    call_number = models.CharField(
        "Call No.", max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.title + " " + self.author


class BookPhotos(models.Model):
    book = models.ForeignKey(
        Book, related_name='book_photos', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='shop-pictures/', blank=True, null=True)


class BookRate(models.Model):
    class Meta:
        unique_together = ['book', 'user']

    user = models.ForeignKey(
        User, related_name='user_rate', on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book, related_name='book_rate', on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                      MaxValueValidator(5)])

    def __str__(self) -> str:
        return self.book.title + " - " + str(self.rate)


class BookSaved(models.Model):
    class Meta:
        unique_together = ['book', 'user']

    user = models.ForeignKey(
        User, related_name='user_book_save', on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book, related_name='book_book_save', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.book.title


class BookViewCount(models.Model):
    class Meta:
        unique_together = ['book', 'user']

    user = models.ForeignKey(
        User, related_name='user_book_view_count', on_delete=models.CASCADE)

    book = models.ForeignKey(
        Book, related_name='book_book_view_count', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
