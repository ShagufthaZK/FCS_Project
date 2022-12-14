# Generated by Django 3.2.16 on 2022-11-28 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_sharedfiles_digital_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='amountshared',
            name='prescription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sharedfiles'),
        ),
        migrations.CreateModel(
            name='PharmacyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('prescription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.sharedfiles')),
            ],
        ),
    ]
