# Generated by Django 5.1.2 on 2025-03-30 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library_service", "0019_alter_librarysettings_holidays"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="analogous_order_item",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="library_service.orderitem"
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="description",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
