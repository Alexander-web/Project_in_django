# Generated by Django 2.2.4 on 2019-10-04 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20191004_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssi',
            name='band_frequency',
            field=models.FloatField(verbose_name='Полоса частот'),
        ),
    ]
