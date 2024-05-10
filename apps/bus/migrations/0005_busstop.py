# Generated by Django 4.2.7 on 2024-05-10 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bus", "0004_alter_busroute_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="BusStop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_safe_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=255)),
                ("map_location", models.CharField(max_length=255)),
                ("departure_time", models.TimeField(verbose_name="Departure Time")),
                ("arrival_time", models.TimeField(verbose_name="Arrival Time")),
                (
                    "bus_route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bus_stops",
                        to="bus.busroute",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
