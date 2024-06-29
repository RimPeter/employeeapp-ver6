# Generated by Django 4.2.13 on 2024-06-29 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='JobsDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(choices=[('painting', 'Painting'), ('drywall_installation', 'Drywall Installation'), ('flooring', 'Flooring'), ('plumbing', 'Plumbing'), ('electrical_work', 'Electrical Work'), ('carpentry', 'Carpentry'), ('hvac_installation', 'HVAC Installation'), ('tile_work', 'Tile Work'), ('cabinet_installation', 'Cabinet Installation'), ('insulation', 'Insulation'), ('lighting_installation', 'Lighting Installation'), ('window_installation', 'Window Installation'), ('door_installation', 'Door Installation'), ('bathroom_remodeling', 'Bathroom Remodeling'), ('kitchen_remodeling', 'Kitchen Remodeling')], max_length=50)),
                ('job_done_in_hours', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='jobs_done', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClockIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('clock_out_time', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeapp.employee')),
            ],
        ),
    ]
