# Generated by Django 5.0.4 on 2024-08-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_wastepickup_pickup_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wastepickup',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Picked up', 'Picked up'), ('Cancelled', 'Cancelled')], default='Pending', max_length=253),
        ),
        migrations.AlterField(
            model_name='wastepickup',
            name='waste_type',
            field=models.CharField(choices=[('RECYCLABLE', 'RECYCLABLE'), ('NON_RECYCLABLE', 'NON_RECYCLABLE')], max_length=253),
        ),
    ]
