# Generated by Django 2.2.4 on 2019-09-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190925_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measuretype',
            name='name',
            field=models.CharField(choices=[('1', 'afc'), ('2', 'pos'), ('3', 'amam'), ('4', 'gd')], max_length=50, verbose_name='Тип измерения'),
        ),
    ]
