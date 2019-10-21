# Generated by Django 2.2.4 on 2019-10-21 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeasureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тип измерения')),
            ],
        ),
        migrations.CreateModel(
            name='SSI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Имя SSI')),
                ('input_frequency', models.FloatField(verbose_name='Входная частота')),
                ('output_frequency', models.FloatField(verbose_name='Выходная частота')),
                ('band_frequency', models.FloatField(verbose_name='Полоса частот')),
                ('available_meas', models.ManyToManyField(related_name='ssi', to='app.MeasureType', verbose_name='Тип измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Measure_que',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('meastype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MeasureType', verbose_name='Тип измерения')),
                ('ssi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SSI', verbose_name='Имя SSI')),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('mea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measure_type', to='app.MeasureType', verbose_name='Тип измерения')),
                ('ssi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meas', to='app.SSI', verbose_name='Имя SSI')),
            ],
            options={
                'permissions': (('make_measures', 'проводит измерения'),),
            },
        ),
        migrations.CreateModel(
            name='FreqRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_range', models.CharField(max_length=50, verbose_name='Входной диапазон')),
                ('output_range', models.CharField(max_length=50, verbose_name='Выходной диапазон')),
                ('name', models.CharField(max_length=50, verbose_name='Имя диапазона')),
                ('ssi_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='freqrange', to='app.SSI')),
            ],
        ),
        migrations.CreateModel(
            name='AcceptData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xy', models.TextField(verbose_name='Полученные данные x,y')),
                ('measurement_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m', to='app.Measure')),
            ],
        ),
    ]
