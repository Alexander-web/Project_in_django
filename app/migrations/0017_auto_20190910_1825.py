# Generated by Django 2.2.4 on 2019-09-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_measuretype_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssi',
            name='meas_type',
            field=models.ManyToManyField(related_name='meas', to='app.MeasureType'),
        ),
    ]
