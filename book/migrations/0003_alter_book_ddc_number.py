# Generated by Django 3.2.22 on 2024-02-27 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20240227_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ddc_number',
            field=models.CharField(max_length=50, verbose_name='DDC No.'),
        ),
    ]