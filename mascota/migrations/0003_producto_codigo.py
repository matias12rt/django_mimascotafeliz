# Generated by Django 4.1.2 on 2024-07-06 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota', '0002_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(default='default_value', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
