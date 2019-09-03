from django.shortcuts import render
from .client.tcp_client import send_and_return
from .models import *
from django.http import HttpResponse

    # Представление
def view_list(request):
    # l=[]
    data=send_and_return('measure_afc')
    data=data.replace(',', '.')
    data=data[0:data.__len__()-2]
    s=data.split(';')
    s=s[1:]
    for i in s:
        xy = i.split(':')
        x=float(xy[0])
        y=float(xy[1])
        # l.append('x: {} ; y: {}'.format(x,y))
        MeasureData.objects.create(x=x, y=y)
    return HttpResponse("Ok")

def get_data(request):
    data=[]
    d = list(SSI.objects.values('name','measurement_type'))
    for i in d:
        data.append('{}: измерение {}'.format(i['name'],i['measurement_type']))
    context={
        "data": data
    }
    return render(request, 'app/list.html', context)
    # context={
    # 'l':l,  
    # }
    # return render(request,'app/list.html', context)

    # context={
    #     'x1':x1,  
    #     # 'y1':y1
    #     }

    # return render(request,'app/list.html', context)

# class Client:
#     address_to_server = ('localhost', 49536)
#     sock = socket.socket()
#     def connect(self,sent):
#         self.sock.send(bytes(sent,encoding='UTF-8'))
# request,'app/list.html', context


    # SSIs = SSI.objects.all()
    # MeasureTypes=MeasureType.objects.all()
    # MeasureResults=MeasureResult.objects.all()
    # MeasureDatas=MeasureData()
    # context ={
    #     'SSIs':SSIs,
    #     'MeasureTypes':MeasureType,
    #     'MeasureResults':MeasureResult
    # }
    
        
