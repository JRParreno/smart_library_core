# Generated by Django 3.2.22 on 2024-03-30 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_auto_20240323_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='semester',
            field=models.CharField(choices=[('FIRST_SEM', 'First Semester'), ('SECOND_SEM', 'Second Semester')], default='FIRST_SEM', max_length=15),
        ),
        migrations.AlterField(
            model_name='book',
            name='year_level',
            field=models.CharField(choices=[('FIRST_YEAR', 'First Year'), ('SECOND_YEAR', 'Second Year'), ('THIRD_YEAR', 'Third Year'), ('FOURTH_YEAR', 'Fourth Year')], default='FIRST_YEAR', max_length=15),
        ),
    ]
