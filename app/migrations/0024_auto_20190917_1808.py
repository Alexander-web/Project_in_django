# Generated by Django 2.2.4 on 2019-09-17 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20190917_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ssi',
            name='meas_type',
        ),
        migrations.AddField(
            model_name='ssi',
            name='available_meas',
            field=models.ManyToManyField(related_name='ssi', to='app.MeasureType', verbose_name='Тип измерения'),
        ),
        migrations.AlterField(
            model_name='measure_que',
            name='meastype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measure', to='app.MeasureType', verbose_name='Тип измерения'),
        ),
        migrations.AlterField(
            model_name='measure_que',
            name='ssi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meas', to='app.SSI', verbose_name='Имя SSI'),
        ),
        migrations.AlterField(
            model_name='measuretype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Тип измерения'),
        ),
        migrations.AlterField(
            model_name='ssi',
            name='band_frequency',
            field=models.IntegerField(verbose_name='Полоса частот'),
        ),
        migrations.AlterField(
            model_name='ssi',
            name='input_frequency',
            field=models.IntegerField(verbose_name='Входная частота'),
        ),
        migrations.AlterField(
            model_name='ssi',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя SSI'),
        ),
        migrations.AlterField(
            model_name='ssi',
            name='output_frequency',
            field=models.IntegerField(verbose_name='Выходная частота'),
        ),
    ]
