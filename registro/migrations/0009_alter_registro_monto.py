# Generated by Django 4.2.20 on 2025-04-06 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registro", "0008_alter_registro_monto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registro",
            name="monto",
            field=models.CharField(default="0", max_length=5, unique=True),
        ),
    ]
