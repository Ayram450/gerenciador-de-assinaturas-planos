# Generated by Django 5.2.3 on 2025-07-08 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0002_rename_categoria_subscription_metpagar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="categoria",
            field=models.CharField(default="default", max_length=50),
            preserve_default=False,
        ),
    ]
