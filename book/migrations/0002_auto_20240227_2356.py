# Generated by Django 3.2.22 on 2024-02-27 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='call_number',
            field=models.CharField(max_length=50, verbose_name='Call No.'),
        ),
        migrations.AlterField(
            model_name='book',
            name='control_number',
            field=models.CharField(max_length=50, verbose_name='Control No.'),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition_statement',
            field=models.CharField(max_length=250, verbose_name='Edition Statement'),
        ),
        migrations.AlterField(
            model_name='book',
            name='general_information',
            field=models.TextField(default='', verbose_name='General Information'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn_issn',
            field=models.IntegerField(verbose_name='ISBN/ISSN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='physical_description',
            field=models.CharField(max_length=255, verbose_name='Physical Description'),
        ),
    ]
