# Generated by Django 3.2.22 on 2024-02-28 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20240228_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='call_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Call No.'),
        ),
        migrations.AlterField(
            model_name='book',
            name='control_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Control No.'),
        ),
    ]