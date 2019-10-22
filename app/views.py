from django.shortcuts import render
from .client_server.tcp_client import send_and_return
import threading 
from django.shortcuts import redirect
from .models import *
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
import json

#Функция отвечает за нормировку даных для графиков (возвращает данные в класс Meas_graph для дальнейшего преобразования в json)
def norm_data(data_id,mt_name):
    xydata=[]
    x1=[]
    y1=[]
    data=AcceptData.objects.get(id=data_id)
    parse_data=data.xy
    parse_data=parse_data.replace(',', '.')
    parse_data=parse_data[0:parse_data.__len__()-2]
    parse=parse_data.split(';')
    if (mt_name =='afc'):
        f0=parse.pop(0)
        f0=f0.split(':')
        f1=f0[1]
        for i in parse:
            xy = i.split(':')
            x1.append(float(xy[0]))
            y1.append(float(xy[1]))
    #Нормировка по уровню (мощность) + частота для АЧХ
        for i,j in zip(y1,x1):
            data_dict={}
            p=max(y1)-i
            h=j-float(f1)
            data_dict.update({"x": h, "y": p})
            xydata.append(data_dict)
        return xydata
    if mt_name == ('gd'):
        f0=parse.pop(0)
        f0=f0.split(':')
        f1=f0[1]
        for i in parse:
            xy = i.split(':')
            x1.append(float(xy[0]))
            y1.append(float(xy[1]))
    #Нормировка НГВЗ частота + уровень(время)
        for i,j in zip(y1,x1):
            data_dict={}
            p=min(y1)-i
            h=j-float(f1)
            data_dict.update({"x": h, "y": p})
            xydata.append(data_dict)
        return xydata
    else:
        for i in parse:
            data_dict={}
            xy = i.split(':')
            data_dict.update({"x": float(xy[0]), "y": float(xy[1])})
            xydata.append(data_dict)
        return xydata

#Класс отвечает за создание потока, который используется для сервера (вызывается в классе Make_measures)
class Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        from .client_server.tcp_server import create_data
        data = create_data
        return data

#Добавляет измерения в очередь
class MeasuresData(TemplateView):
    def get(self,req,meas_name,ssi_name):
        ssi=SSI.objects.get(name=ssi_name)
        meas=MeasureType.objects.get(name=meas_name)
        new_element=Measure_que.objects.create(ssi=ssi,meastype=meas)
        return redirect('ssi_list')

#Отвечает за отрисовку общего листа со списком SSI
class SSIList(LoginRequiredMixin,TemplateView):
    template_name = 'app/index.html'
    def get(self,req):
        context={}
        context['ssi'] = SSI.objects.all()
        context['planed_measure'] = Measure_que.objects.all()
        context['freq']=FreqRange.objects.order_by().values_list('name', flat=True).distinct()
        context['SSI']=SSI.objects.all()
        context['accept_data']=AcceptData.objects.all()
        return render(req, self.template_name,context)

#Удаляет запланированные измерения из очереди
class Remove_from_que(TemplateView):
    def get(self,req,name_remove):
        Measure_que.objects.get(id=name_remove).delete()
        return redirect('ssi_list')

#Отвечает за удаление уже проведенного измерения по нажатию кнопки
class Remove_from_measure(TemplateView):
    def get(self,req,name):
        Measure.objects.get(id=name).delete()
        return redirect('ssi_list')

#Удаляет SSI добавленный через форму
class  Remove_from_ssilist(TemplateView):
    def get(self,req,id_name):
        SSI.objects.get(id=id_name).delete()
        return redirect('create')

#Этот класс отвечает за рендеринг домашней страницы
class Baselist(LoginRequiredMixin,TemplateView):
    template_name = 'app/base.html'
    def get(self,req):
        context={}
        # context['ssi_name'] = SSI.objects.all()
        return render(req, self.template_name,context)

#Класс, отвечающий за представление help
class Helplist(TemplateView):
    template_name = 'app/help.html'
    def get(self,req):
        context={}
        # context['ssi_name'] = SSI.objects.all()
        return render(req, self.template_name,context)

#Этот класс отвечает за представление информации о SSI из таблицы
class SSIDetail(TemplateView):
    template_name = 'app/ssi_detail.html'
    def get(self,req,ssi):
        context={}
        context['ssi'] = SSI.objects.get(name = ssi)
        return render(req, self.template_name,context)

#Класс, проделывающий измерения
class Make_measures(PermissionRequiredMixin,TemplateView):
    permission_required = 'catalog.make_measures'
    def get(self,req):
        meas=Measure_que.objects.all()
        mea=Measure.objects.all()
        for m in meas:
            me=str(m.meastype)
            thread1 = Thread()
            thread1.start()
            # thr = threading.Thread(target=start_server, args=(me,))
            # thr.setDaemon(True)
            # thr.start()
            data_current=send_and_return(me)
            new_element=Measure.objects.create(ssi=m.ssi,mea=m.meastype)
            measurement_data_current=new_element
            new_measures=AcceptData.objects.create(measurement_data =measurement_data_current, xy=data_current)
            m.delete()
        return redirect('ssi_list')

#Класс отвечающий за вывод информации о проведенных измерениях
class Meas_info(TemplateView):
    template_name = 'app/measure_info.html'
    def get(self,req,mt_name,ssi_info_name,id_measure):
        context={}
        context['mt_name']=mt_name
        context['ssi_name']=ssi_info_name
        context['data']=AcceptData.objects.get(id=id_measure)
        context['data_id']=id_measure
        return render(req,self.template_name,context)

#Класс выдает json данные, взятые из БД, библиотеке feth 
class Meas_graph(TemplateView):
    def get(self,req,data_id,mt_name):
        evidence=norm_data(data_id,mt_name)
        json_data=json.dumps(evidence)
        return HttpResponse(json_data)

#Представление (функция) отвечающя за взаимодействие с формой
@login_required
def ssi_new(req):
    template_name = 'app/create_config.html'
    if req.method == "POST":
        form = SSIform(req.POST)
        if form.is_valid():
            ssi = form.save()
            if ssi.input_frequency >= 0 and ssi.input_frequency <= 1.8:
                inputfreq="L"
            elif ssi.input_frequency >= 1.9 and ssi.input_frequency <= 3.3:
                inputfreq="S"
            elif ssi.input_frequency >= 3.4 and ssi.input_frequency <= 5.724:
                inputfreq="C-low"
            elif ssi.input_frequency >= 5.725 and ssi.input_frequency <= 7.24:
                inputfreq="C-high"
            elif ssi.input_frequency >= 7.25 and ssi.input_frequency <= 10.6:
                inputfreq="X"
            elif ssi.input_frequency >= 10.7 and ssi.input_frequency <= 15.3:
                inputfreq="Ku"
            elif ssi.input_frequency >= 15.4 and ssi.input_frequency <= 26:
                inputfreq="K"
            elif ssi.input_frequency >= 27 and ssi.input_frequency <= 64:
                inputfreq="Ka"
            elif ssi.input_frequency >= 65 and ssi.input_frequency <= 110:
                inputfreq="W" 
                
            if ssi.output_frequency >= 0 and ssi.output_frequency <= 1.8:
                outputfreq="L"
            elif ssi.output_frequency >= 1.9 and ssi.output_frequency <= 3.3:
                outputfreq="S"
            elif ssi.output_frequency >= 3.4 and ssi.output_frequency <= 5.724:
                outputfreq="C-low"
            elif ssi.output_frequency >= 5.725 and ssi.output_frequency <= 7.24:
                outputfreq="C-high"
            elif ssi.output_frequency >= 7.25 and ssi.output_frequency <= 10.6:
                outputfreq="X"
            elif ssi.output_frequency >= 10.7 and ssi.output_frequency <= 15.3:
                outputfreq="Ku"
            elif ssi.output_frequency >= 15.4 and ssi.output_frequency <= 27.4:
                outputfreq="K"
            elif ssi.output_frequency >= 27.5 and ssi.output_frequency <= 64:
                outputfreq="Ka"
            elif ssi.output_frequency >= 65 and ssi.output_frequency <= 110:
                outputfreq="W"
            new_ssi_element=ssi
            new_freqrange=FreqRange.objects.create(input_range=inputfreq, output_range=outputfreq, ssi_element=new_ssi_element, name="{}/{}".format(inputfreq,outputfreq))
            return redirect('create')
    else:
        form = SSIform()
        context = {}
        context['form']=form
        # context['freq']=FreqRange.objects.values_list('input_range','output_range').distinct()
        context['Freqmodel']=FreqRange.objects.all()
        return render(req,template_name,context)

#Функция отрисовывает html с отсартированными данными + выводит пункты меню выбора
def freq_sort(req):
    template_name = 'app/filter.html'
    if req.method == "POST":
        frm = Formfilter(req.POST)
        if frm.is_valid():
            freq=frm.cleaned_data['choice']
            sort=FreqRange.custom_manager.get_queryset(freq)
            context = {}
            context['planed_measure'] = Measure_que.objects.all()
            context['Freqmodel']=sort
            context['freq']=FreqRange.objects.order_by().values_list('name', flat=True).distinct()
            if frm.cleaned_data['choice'] == 'all':
                return redirect('ssi_list')
            else:
                return render(req,template_name,context)


















        # context['data_for_form']=Form_for_choice.objects.order_by().values_list('input_range','output_range', flat=True).distinct()



            # new_freqrange=FreqRange.objects.create(input_range=ssi.input_frequency, output_range=ssi.output_frequency)
            # ssi.freqrange=new_freqrange
            # ssi.save()
#Класс отвечает за форму для сортировки частотных диапазонов

# def freq_sort(req):
#     template_name = 'app/create_config.html'
#     if req.method == "POST":
#         frm = Formfilter(req.POST)
#         if frm.is_valid():
#             freq=frm.cleaned_data['choice']
#             sort=FreqRange.custom_manager.get_queryset(freq)
#             context = {}
#             form = SSIform()
#             context['form']=form
#             context['Freqmodel']=sort
#             context['freq']=FreqRange.objects.order_by().values_list('name', flat=True).distinct()
#             context['chek']=freq
#             if frm.cleaned_data['choice'] == 'all':
#                 return redirect('create')
#             else:
#                 return render(req,template_name,context)
#             # return redirect('create')