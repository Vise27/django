# Generated by Django 5.0 on 2024-11-20 05:36

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('correo', models.EmailField(max_length=255, null=True)),
                ('direccion', models.CharField(max_length=255, null=True)),
                ('nombre', models.CharField(max_length=255, null=True)),
                ('telefono', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id_carrito', models.BigAutoField(primary_key=True, serialize=False)),
                ('creado_en', models.DateTimeField(default=django.utils.timezone.now)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.BigAutoField(primary_key=True, serialize=False)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.carrito')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(null=True, upload_to='imagenes_productos/')),
                ('nombre', models.CharField(max_length=255, null=True)),
                ('precio', models.FloatField(null=True)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.categoria')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.producto')),
            ],
        ),
        migrations.CreateModel(
            name='CarritoItem',
            fields=[
                ('id_item', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='elsol.carrito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.producto')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroEntrada',
            fields=[
                ('id_registro', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(default=0)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.FloatField(null=True)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.carrito')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.FloatField(null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.venta')),
            ],
        ),
    ]
