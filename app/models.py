from django.conf import settings
from django.db import models
from django.utils import timezone
import socket

class MeasureData(models.Model): # X-Y данные
    x = models.FloatField()
    y = models.FloatField()
    def __str__(self):
        return 'x:{} - y:{}'.format(self.x, self.y)

class MeasureType(models.Model):               #Тип измерерия АЧХ, НГВЗ, точка насыщения, АМ-АМ
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class SSI(models.Model): 
    name = models.CharField(max_length=50)                  #Конфигурации
    input_frequency = models.IntegerField()
    output_frequency = models.IntegerField()
    band_frequency = models.IntegerField()
    measurement_type = models.ManyToManyField(MeasureType, related_name = 'meas_result')
    def __str__(self):
        return self.name

class MeasureResult(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    ssi = models.ForeignKey(SSI, on_delete = models.CASCADE)
    mesure_type = models.ForeignKey(MeasureType, on_delete = models.CASCADE)
    measurement_data = models.ManyToManyField(MeasureData, related_name = 'meas_result')
    def __str__(self):
        return 'ssi: {}, тип измерения: {}, время измерения: {}'.format(self.ssi, self.mesure_type, self.date_time)
































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

