# Generated by Django 5.1.6 on 2025-05-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("measurement", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sensor",
            name="description",
            field=models.CharField(blank=True, max_length=255, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="sensor",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Название"),
        ),
    ]
