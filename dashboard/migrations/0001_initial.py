# Generated by Django 5.0.4 on 2024-09-30 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveSensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bin_id', models.CharField(max_length=120)),
                ('humidity', models.FloatField()),
                ('waste_height', models.FloatField()),
                ('temperature', models.FloatField()),
                ('weight', models.FloatField()),
                ('batt_value', models.FloatField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='WasteBin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('reward_points', models.IntegerField(default=0, null=True)),
                ('battery_level', models.IntegerField(null=True)),
                ('charge_status', models.BooleanField(null=True)),
                ('power_consumption', models.FloatField(null=True)),
                ('battery_status', models.IntegerField(null=True)),
                ('picked_up', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BinCompartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_waste', models.CharField(choices=[('RECYCLABLE', 'RECYCLABLE'), ('NON_RECYCLABLE', 'NON_RECYCLABLE')], max_length=20)),
                ('temperature', models.FloatField(null=True)),
                ('weight', models.FloatField(default=0, null=True)),
                ('bin_level', models.IntegerField(null=True)),
                ('new_field', models.BooleanField(default=False)),
                ('parent_bin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compartments', to='dashboard.wastebin')),
            ],
        ),
        migrations.CreateModel(
            name='WasteBinRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('pending', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WastePickUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waste_type', models.CharField(choices=[('RECYCLABLE', 'RECYCLABLE'), ('NON_RECYCLABLE', 'NON_RECYCLABLE')], max_length=253)),
                ('reward_gained', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Picked up', 'Picked up'), ('Cancelled', 'Cancelled')], default='Pending', max_length=253)),
                ('pickup_date_time', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_picked', models.DateTimeField()),
                ('parent_bin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.wastebin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
