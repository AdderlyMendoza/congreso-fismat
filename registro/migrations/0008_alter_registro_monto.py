# Generated by Django 4.2.20 on 2025-04-06 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registro", "0007_registro_monto_alter_registro_doc_acreditivo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registro",
            name="monto",
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
