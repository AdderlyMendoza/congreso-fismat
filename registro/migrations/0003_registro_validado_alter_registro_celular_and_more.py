# Generated by Django 4.2 on 2025-03-02 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registro", "0002_alter_registro_proyecto_investigacion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="registro",
            name="validado",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="registro",
            name="celular",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name="registro",
            name="dni",
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name="registro",
            name="proyecto_investigacion",
            field=models.FileField(upload_to="pdfs/"),
        ),
    ]
