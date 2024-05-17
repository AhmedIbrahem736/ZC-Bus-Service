# Generated by Django 4.2.7 on 2024-05-16 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("semester", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="semester",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="semester",
            name="is_safe_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="semester",
            name="modified_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
