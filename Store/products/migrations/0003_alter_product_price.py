# Generated by Django 5.0.2 on 2024-02-10 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_order_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Narx'),
        ),
    ]
