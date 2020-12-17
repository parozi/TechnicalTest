# Generated by Django 2.2.13 on 2020-12-17 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Bond",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("isin", models.CharField(max_length=12)),
                ("currency", models.CharField(max_length=3)),
                ("maturity", models.DateField()),
                ("lei", models.CharField(max_length=20)),
                ("legal_name", models.CharField(max_length=255)),
                ("size", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=11, unique=True, verbose_name="Phone Number"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "bond",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bonds.Bond"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
