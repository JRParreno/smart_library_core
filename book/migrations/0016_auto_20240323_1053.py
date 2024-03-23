# Generated by Django 3.2.22 on 2024-03-23 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_auto_20240323_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='semester',
            field=models.CharField(choices=[('FIRST_SEM', 'First Semester'), ('SECOND_SEM', 'Second Semester')], default='FIRST', max_length=15),
        ),
        migrations.AlterField(
            model_name='book',
            name='year_level',
            field=models.CharField(choices=[('FIRST_YEAR', 'First Year'), ('SECOND_YEAR', 'Second Year'), ('THIRD_YEAR', 'Third Year'), ('FOURTH_YEAR', 'Fourth Year')], default='FIRST', max_length=15),
        ),
    ]
