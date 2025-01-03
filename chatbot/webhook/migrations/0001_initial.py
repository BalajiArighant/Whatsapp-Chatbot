# Generated by Django 5.1.4 on 2024-12-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("user_id", models.CharField(max_length=100)),
                ("user_name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=100)),
                ("kovil", models.CharField(max_length=100)),
                ("native_place", models.CharField(max_length=100)),
                ("current_location", models.CharField(max_length=100)),
                ("token_number", models.IntegerField()),
            ],
        ),
    ]
