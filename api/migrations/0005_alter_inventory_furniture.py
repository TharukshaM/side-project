# Generated by Django 5.1.6 on 2025-02-19 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_remove_furniture_stock_alter_inventory_furniture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="furniture",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.furniture"
            ),
        ),
    ]
