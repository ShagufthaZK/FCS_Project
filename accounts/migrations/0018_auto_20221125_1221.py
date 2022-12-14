# Generated by Django 3.0.5 on 2022-11-25 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_symptoms_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='symptoms',
            old_name='shared_to',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='symptoms',
            name='completed',
        ),
        migrations.CreateModel(
            name='SymptomsShared',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('symp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Symptoms')),
            ],
        ),
    ]
