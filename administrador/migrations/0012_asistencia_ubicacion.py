# Generated by Django 4.2.20 on 2025-05-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0011_alter_asistencia_entrada_alter_asistencia_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='ubicacion',
            field=models.CharField(choices=[('A', 'Lugar A'), ('B', 'Lugar B'), ('C', 'Lugar C'), ('D', 'Lugar D')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
