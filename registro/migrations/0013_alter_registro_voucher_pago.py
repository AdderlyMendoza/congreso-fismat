# Generated by Django 4.2.20 on 2025-04-14 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0012_alter_registro_tipo_participante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='voucher_pago',
            field=models.FileField(blank=True, default=1, upload_to='pdfs/'),
            preserve_default=False,
        ),
    ]
