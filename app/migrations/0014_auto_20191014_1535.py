# Generated by Django 2.2.4 on 2019-10-14 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20191014_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssi',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя SSI'),
        ),
    ]
