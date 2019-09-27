from django.shortcuts import render
from .client_server.tcp_client import send_and_return
from django.shortcuts import redirect
from .models import *
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import SSIform

#Добавляет измерения в очередь
class MeasuresData(TemplateView):
    def get(self,req,meas_name,ssi_name):
        ssi=SSI.objects.get(name=ssi_name)
        meas=MeasureType.objects.get(name=meas_name)
        new_element=Measure_que.objects.create(ssi=ssi,meastype=meas)
        return redirect('ssi_list')

#Отвечает за отрисовку общего листа со списком SSI
class SSIList(TemplateView):
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
class Baselist(TemplateView):
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
class Make_measures(TemplateView):
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
def ssi_new(req):
    template_name = 'app/create_config.html'
    if req.method == "POST":
        form = SSIform(req.POST)
        if form.is_valid():
            ssi = form.save()
            return redirect('create')
    else:
        form = SSIform()
        context = {}
        context['form']=form
        context['ssi']=SSI.objects.all()
        return render(req,template_name,context)

