# Generated by Django 3.2.16 on 2022-10-31 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_userfiles_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfiles',
            name='user',
        ),
    ]