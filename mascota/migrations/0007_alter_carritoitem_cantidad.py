# Generated by Django 4.1.2 on 2024-07-19 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota', '0006_carrito_carritoitem_carrito_productos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carritoitem',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
