# Generated by Django 4.1.7 on 2023-03-22 19:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0018_booking_total_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="Eventbooking",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("date_booked", models.DateTimeField(auto_now_add=True)),
                (
                    "featured_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("payment_status", models.BooleanField(default=False)),
                (
                    "event_page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.eventpage"
                    ),
                ),
            ],
        ),
    ]
