# Generated by Django 4.1.2 on 2022-10-30 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_product_address_remove_product_medicine_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='pharmacy_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
