# Generated by Django 3.2.16 on 2022-10-26 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221026_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
