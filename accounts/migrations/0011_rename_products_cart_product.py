# Generated by Django 4.1.2 on 2022-10-31 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_cart_quantity_alter_cart_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='products',
            new_name='product',
        ),
    ]
