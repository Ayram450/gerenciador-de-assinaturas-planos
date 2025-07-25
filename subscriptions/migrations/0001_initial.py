# Generated by Django 5.2.3 on 2025-06-16 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subscription",
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
                ("nomePlano", models.CharField(max_length=100)),
                ("empresa", models.CharField(max_length=100)),
                ("data_venc", models.DateTimeField()),
                ("categoria", models.CharField(max_length=50)),
                ("valorMens", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
