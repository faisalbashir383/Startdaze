# Generated by Django 5.0.3 on 2024-12-15 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0003_activity_hotel_hotelimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='popularity_score',
            new_name='total_trips',
        ),
    ]
