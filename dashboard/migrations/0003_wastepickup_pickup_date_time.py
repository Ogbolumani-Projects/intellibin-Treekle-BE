# Generated by Django 5.0.4 on 2024-08-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_wastepickup_confirmed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastepickup',
            name='pickup_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]