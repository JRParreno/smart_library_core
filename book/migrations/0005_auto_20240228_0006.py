# Generated by Django 3.2.22 on 2024-02-28 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_isbn_issn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='imprint',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='physical_description',
            field=models.TextField(verbose_name='Physical Description'),
        ),
    ]
