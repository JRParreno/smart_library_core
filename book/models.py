import datetime
from django.db import models
from department.models import Department
from django.core.validators import MaxValueValidator, MinValueValidator


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
    iso = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(default='')
    number_copies = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    tags = models.ManyToManyField(Tags, null=True, blank=True)

    def __str__(self) -> str:
        return self.title + " " + self.title


class BookPhotos(models.Model):
    book = models.ForeignKey(
        Book, related_name='book_photos', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='shop-pictures/', blank=True, null=True)