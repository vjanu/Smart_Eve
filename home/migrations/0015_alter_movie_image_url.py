# Generated by Django 4.1.7 on 2023-02-22 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0014_alter_movie_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="image_url",
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
    ]
