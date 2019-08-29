from django.shortcuts import render
from django.utils import timezone
from .models import *
# import socket
# import numpy, math

def list(request,i):
    address_to_server = ('localhost', 49536)
    sock = socket.socket()
    sock.send(bytes('measure_afc',encoding='UTF-8'))
    while True:
        data = sock.recv(1024)
        d = data.decode("utf-8")
        d = str(d)
    s = d.split(';')
    for i in s:
        xy = i.split(':')
        xx = float(xy[0])
        yy = float(xy[1])
        p = Measure(x=xx, y= yy)
        p.save()
    books = Book.objects.all()
    genres = Genre.objects.all()
    pub= Publish.objects.all()
    context ={
        'books':books,
        'genres':genres,
        'pub':pub
    }
    return render(request,'app/list.html', context)

class Client:
    address_to_server = ('localhost', 49536)
    sock = socket.socket()
    def connect(self,sent):
        self.sock.send(bytes(sent,encoding='UTF-8'))
    
        
