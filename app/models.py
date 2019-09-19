from django.conf import settings
from django.db import models
from django.utils import timezone
import socket


class MeasureType(models.Model):               #Тип измерерия АЧХ, НГВЗ, точка насыщения, АМ-АМ
    name = models.CharField(max_length=50,verbose_name="Тип измерения")
    def __str__(self):
        return self.name

class SSI(models.Model):                                #Конфигурации
    name = models.CharField('Имя SSI',max_length=50)                  
    input_frequency = models.IntegerField('Входная частота')
    output_frequency = models.IntegerField('Выходная частота')
    band_frequency = models.IntegerField('Полоса частот')
    available_meas= models.ManyToManyField(MeasureType, related_name='ssi',verbose_name="Тип измерения")
    def __str__(self):
        return self.name

class Measure_que(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE, verbose_name="Имя SSI")
    meastype = models.ForeignKey(MeasureType, on_delete = models.CASCADE,verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}, Время измерения: {}'.format(self.ssi, self.meastype, self.date_time)

class Measure(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE,related_name='meas', verbose_name="Имя SSI")
    mea = models.ForeignKey(MeasureType, on_delete = models.CASCADE,related_name = 'measure_type',verbose_name="Тип измерения")
    def __str__(self):
        return 'Имя SSI: {}, Тип измерения: {}'.format(self.ssi, self.mea)

class AcceptData(models.Model): # X-Y данные
    measurement_data = models.ForeignKey(Measure, on_delete = models.CASCADE, related_name = 'meas_result',default=1)
    xy = models.TextField('Полученные данные x,y')

































# class Genre(models.Model):
#     genre_name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.genre_name
#     def com(self):
#         self.save()

# class Publish(models.Model):
#     publish_name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.publish_name
#     def com(self):
#         self.save()   

# class Book(models.Model):
#     title = models.CharField(max_length=50)
#     genre = models.ForeignKey("Genre",on_delete=models.CASCADE)
#     publ = models.ForeignKey("Publish",on_delete=models.CASCADE)
#     created_date = models.DateTimeField(default=timezone.now)
#     def com(self):
#         self.save()   
#     def __str__(self):
#         return self.title

# class Measure(models.Model):
#     x = models.FloatField()
#     y = models.FloatField()
#     def com(self):
#         self.save()   
#     def __str__(self):
#         return self.x.__str__ + '/' + self.y.__str__

