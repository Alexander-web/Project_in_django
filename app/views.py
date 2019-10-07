from django.shortcuts import render
from .client_server.tcp_client import send_and_return
from django.shortcuts import redirect
from .models import *
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import SSIform
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
# from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

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
        return render(req,self.template_name,context)

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
            new_freqrange=FreqRange.objects.create(input_range=inputfreq, output_range=outputfreq, ssi_element=new_ssi_element)
            return redirect('create')
    else:
        form = SSIform()
        context = {}
        context['form']=form
        context['ssi']=SSI.objects.all()
        return render(req,template_name,context)


# Класс, отвечающий за сортировку элементов таблицы по частотным диапазонам
#Модель, отвечающая за переопределение стандартного менеджера модели FreqRange
class Sort(TemplateView):
    template_name = "app/create_config"
    def get(self,req,value):
        class Sortfreq(models.Manager):
            def get_queryset(self):
                return super(Sortfreq, self).get_queryset().filter(author='Roald Dahl')
        context={}
        context['freq']=SSI.objects.all()
        return render(req,template_name,context)




















            # new_freqrange=FreqRange.objects.create(input_range=ssi.input_frequency, output_range=ssi.output_frequency)
            # ssi.freqrange=new_freqrange
            # ssi.save()