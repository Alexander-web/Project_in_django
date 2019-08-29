from django.conf import settings
from django.db import models
from django.utils import timezone
import socket

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    def __str__(self):
        return self.genre_name
    def com(self):
        self.save()

class Publish(models.Model):
    publish_name = models.CharField(max_length=50)
    def __str__(self):
        return self.publish_name
    def com(self):
        self.save()   

class Book(models.Model):
    title = models.CharField(max_length=50)
    genre = models.ForeignKey("Genre",on_delete=models.CASCADE)
    publ = models.ForeignKey("Publish",on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    def com(self):
        self.save()   
    def __str__(self):
        return self.title

class Measure(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    def com(self):
        self.save()   
    def __str__(self):
        return self.x.__str__ + '/' + self.y.__str__

