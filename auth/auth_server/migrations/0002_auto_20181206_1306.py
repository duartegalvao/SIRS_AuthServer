# Generated by Django 2.1.2 on 2018-12-06 13:06

import annoying.fields
from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertwofactor',
            old_name='twofactor_enabled',
            new_name='two_factor_enabled',
        ),
        migrations.RemoveField(
            model_name='usertwofactor',
            name='id',
        ),
        migrations.AlterField(
            model_name='usertwofactor',
            name='user',
            field=annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='two_factor', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
