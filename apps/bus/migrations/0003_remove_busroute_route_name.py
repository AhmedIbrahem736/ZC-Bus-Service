# Generated by Django 4.2.7 on 2024-05-10 15:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bus", "0002_remove_busroute_num_seats_alter_busroute_code_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="busroute",
            name="route_name",
        ),
    ]
