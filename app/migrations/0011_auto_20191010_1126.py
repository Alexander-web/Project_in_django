# Generated by Django 2.2.4 on 2019-10-10 04:26

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_freqrange_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='freqrange',
            managers=[
                ('custom_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
