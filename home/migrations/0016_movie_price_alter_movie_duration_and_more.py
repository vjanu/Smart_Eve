# Generated by Django 4.1.7 on 2023-02-22 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0015_alter_movie_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="price",
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="movie",
            name="duration",
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="image_url",
            field=models.CharField(max_length=100000, null=True),
        ),
    ]
