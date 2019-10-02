from django.conf import settings
from django.db import models
from django.utils import timezone
import socket

class Operator(models.Model):
    name = models.CharField(max_length=50,verbose_name="Имя оператора")
    surname = models.CharField(max_length=50,verbose_name="Фамилия оператора")
    password=models.CharField(max_length=50,verbose_name="Пароль")

class MeasureType(models.Model):                         #Тип измерерия АЧХ, НГВЗ, точка насыщения, АМ-АМ
    name = models.CharField(max_length=50,verbose_name="Тип измерения")
    def __str__(self):
        return self.name

class SSI(models.Model):                                    #Конфигурации
    name = models.CharField('Имя SSI',max_length=50)                  
    input_frequency = models.IntegerField('Входная частота')
    output_frequency = models.IntegerField('Выходная частота')
    band_frequency = models.IntegerField('Полоса частот')
    available_meas= models.ManyToManyField(MeasureType, related_name='ssi',verbose_name="Тип измерения")
    def __str__(self):
        return self.name

class Measure_que(models.Model):                            # Класс очереди
    date_time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE, verbose_name="Имя SSI")
    meastype = models.ForeignKey(MeasureType, on_delete = models.CASCADE,verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}, Время измерения: {}'.format(self.ssi, self.meastype, self.date_time)

class Measure(models.Model):                                #Класс, собирающий информацию о имени SSI и типе измерения в нем для передачи этой информации в AcceptData
    time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE,related_name='meas', verbose_name="Имя SSI")
    mea = models.ForeignKey(MeasureType, on_delete = models.CASCADE,related_name = 'measure_type',verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}'.format(self.ssi, self.mea)

class AcceptData(models.Model):                             # X-Y данные
    xy = models.TextField('Полученные данные x,y')
    measurement_data = models.ForeignKey(Measure, on_delete = models.CASCADE,related_name = 'm')
    def __str__(self):
        return ' Измерения: {}'.format(self.measurement_data)




 

























