# Generated by Django 3.2.22 on 2024-03-23 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Program', 'verbose_name_plural': 'Programs'},
        ),
    ]