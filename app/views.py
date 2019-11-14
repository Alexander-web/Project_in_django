# from django.conf import settings
from django.shortcuts import render 
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
import threading
from .models import *
from .forms import *
from .client_server.tcp_client import send_and_return
from .scpi.afc_gd import create_meas
import json
from .create_pdf.Create_PDF import cr_PDF,plot_graf_in_svg

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

    input_freq = data.measurement_data.ssi.input_frequency*1000
    output_freq = data.measurement_data.ssi.output_frequency*1000
    if (mt_name =='afc'):
        f0=parse.pop(0)
        f0=f0.split(':')
        # f1=f0[1]
        f1=output_freq
        for i in parse:
            xy = i.split(':')
            x1.append(float(xy[0]))
            y1.append(float(xy[1]))
    #Нормировка по уровню (мощность) + частота для АЧХ
        for i,j in zip(y1,x1):
            data_dict={}
            p=i-max(y1)
            h=j-float(f1)
            data_dict.update({"x": h, "y": p})
            xydata.append(data_dict)
        return xydata
    if mt_name == ('gd'):
        f0=parse.pop(0)
        f0=f0.split(':')
        # f1=f0[1]
        f1=output_freq
        for i in parse:
            xy = i.split(':')
            x1.append(float(xy[0]))
            y1.append(float(xy[1]))
    #Нормировка НГВЗ частота + уровень(время)
        for i,j in zip(y1,x1):
            data_dict={}

            len_y_half = round(y1.__len__()/2) # Возвращает половину значений графика gd с округлением к большему
            left_max = y1.index(max(y1[0:len_y_half]))# Ищем максимальное значение в левой половинке графика, проходя от значения 0 до половинки графика len_y_half
            right_max = y1.index(max(y1[len_y_half:]))# Ищем максимальное значение в правой половинке графика, проходя от значения len_y_half до конца графика
            
            p=i-min(y1[left_max:right_max])#Делаем срез y1 от левого максимума до правого и находим в этих значения минимальное значение
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
class Thread(threading.Thread):
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
        form=Choose_device()
        context={}
        context['planed_measure'] = Measure_que.objects.all()
        context['freq']=FreqRange.objects.order_by().values_list('name', flat=True).distinct()
        context['SSI']=SSI.objects.all()
        context['form_for_device']=form
        context['ad']=AcceptData.objects.filter(isvalid=2)
        context['ad_0']=AcceptData.objects.filter(isvalid=0)
        dict_ad={}
        for i in context['ad']:   
            if i.measurement_data.ssi.name not in dict_ad:
                dict_ad[i.measurement_data.ssi.name]=1
            else:
                dict_ad[i.measurement_data.ssi.name]+=1
        context['dict_ad']=dict_ad
        dict_ad_0={}
        for i in context['ad_0']:   
            if i.measurement_data.ssi.name not in dict_ad_0:
                dict_ad_0[i.measurement_data.ssi.name]=1
            else:
                dict_ad_0[i.measurement_data.ssi.name]+=1
        context['dict_ad_0']=dict_ad_0
        return render(req, self.template_name,context)

#Удаляет запланированные измерения из очереди
class Remove_from_que(TemplateView):
    def get(self,req,name_remove):
        Measure_que.objects.get(id=name_remove).delete()
        return redirect('ssi_list')

#Отвечает за удаление уже проведенного измерения по нажатию кнопки
class Remove_from_measure(TemplateView):
    def get(self,req,name,ssiname):
        Measure.objects.get(id=name).delete()
        return redirect('ssi_detail',ssiname)

#Удаляет SSI добавленный через форму
class  Remove_from_ssilist(TemplateView):
    def get(self,req,id_name):
        SSI.objects.get(id=id_name).delete()
        return redirect('create')

#Этот класс отвечает за рендеринг домашней страницы
class Baselist(LoginRequiredMixin,TemplateView):
    template_name = 'app/base.html'
    def get(self,req):
        form=Operatorform()
        form_SpaceCraft=SpaceCraftform()
        form_PayLoad=PayLoadform()
        context={}
        context['operator']=form
        context['spacecraft']=form_SpaceCraft
        context['payload']=form_PayLoad
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
        context['ssi_afc']=context['ssi'].meas.all().filter(mea__name="afc")
        context['ssi_gd']=context['ssi'].meas.all().filter(mea__name="gd")
        context['ssi_amam']=context['ssi'].meas.all().filter(mea__name="amam")
        context['ssi_pos']=context['ssi'].meas.all().filter(mea__name="pos")
        context['SSI'] = SSI.objects.all()
        context['operator']=Operator.objects.all()
        dict_meas={}
        for i in context['ssi'].meas.all():
            if i.mea.name not in dict_meas:
                dict_meas[i.mea.name]=1
            else:
                dict_meas[i.mea.name]+=1
        context['dict_meas']=dict_meas
        return render(req, self.template_name,context)

class Check_valid(TemplateView):
    template_name = 'app/measure_info.html'
    def get(self,req,mt_name,ssi_info_name,id_measure,valid):
        context={}
        context['mt_name']=mt_name
        context['keys']=MeasureType.objects.get(name=mt_name)
        context['ssi_name']=ssi_info_name
        context['data']=AcceptData.objects.get(id=id_measure)
        context['data_id']=id_measure
        context['data'].isvalid=int(valid)
        context['data'].save()
        return render(req,self.template_name,context)

def make_measures(req):
    template_name = 'app/index.html'
    if req.method == "POST":
        form = Choose_device(req.POST)
        if form.is_valid():
            choose=form.cleaned_data['choose']
            meas=Measure_que.objects.all()
            mea=Measure.objects.all()
            for m in meas:
                me=str(m.meastype)
                if choose == 'offline':
                    thread1 = Thread()# Запускаем сервер в отдельном потоке
                    thread1.start()
                    from time import sleep
                    sleep(0.2)
                    data_current=send_and_return(me)
                elif choose == 'real':
                    data_current = create_meas((m.ssi.input_frequency)*10e8,(m.ssi.output_frequency)*10e8,(m.ssi.band_frequency)*10e5,m.meastype.name,201)
                    print(data_current)
                new_element=Measure.objects.create(ssi=m.ssi,mea=m.meastype)
                measurement_data_current=new_element
                new_measures=AcceptData.objects.create(xy=data_current,measurement_data=measurement_data_current,isvalid ='0')
                m.delete()
            return redirect('ssi_list')
        else:
            form = Choose_device()
            context = {}
            context['form_for_device']=form
            return render(req,template_name,context)

#Класс отвечающий за вывод информации о проведенных измерениях
class Meas_info(TemplateView):
    template_name = 'app/measure_info.html'
    def get(self,req,mt_name,ssi_info_name,id_measure):
        context={}
        context['mt_name']=mt_name
        context['ssi_name']=ssi_info_name
        context['data']=AcceptData.objects.get(id=id_measure)
        context['data_id']=id_measure
        context['keys']=MeasureType.objects.get(name=mt_name)
        context['operator']=Operator.objects.all()
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
        keys_form=Keysform()
        measuretype_form=MeasureTypeform()
        context = {}
        context['keys_form']=keys_form
        context['measuretype_form']=measuretype_form
        context['key_data']=Keys.objects.all()
        context['measure_type_data']=MeasureType.objects.all()
        context['Freqmodel']=FreqRange.objects.all()
        context['form']=form
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

def key_create(req):
    if req.method == "POST":
        form = Keysform(req.POST)
        if form.is_valid():
            key = form.save()
    return redirect('create')

def create_measure(req):
    if req.method == "POST":
        form = MeasureTypeform(req.POST)
        if form.is_valid():
            measure_type = form.save()
    return redirect('create')

def create_operator(req):
    if req.method == "POST":
        form = Operatorform(req.POST)
        form_spacecraft = SpaceCraftform(req.POST)
        if form_spacecraft.is_valid() and form.is_valid():
            operator = form.save()
            spacecraft = form_spacecraft.save()
    return redirect('base_list')

def create_payload(req):
    if req.method == "POST":
        form = PayLoadform(req.POST)
        if form.is_valid():
            pay_load = form.save()
    return redirect('base_list')

class Keys_lists(TemplateView):
    template_name = 'app/Keys.html'
    def get(self,req):
        context={}
        context['key']=Keys.objects.all()
        return render(req,self.template_name,context)

class Create_PDF(TemplateView):
    def get(self,req,name_ssi,id_data,name_measure):
        if name_measure=="afc":
            x_name='f, МГц'
            y_name='P, дБ'
            name="АЧХ"
        if name_measure=="gd":
            x_name='f, МГц'
            y_name='t, нс'
            name="ГВЗ"            
        if name_measure=="amam":
            x_name='Pвх, дБ'
            y_name='Pвых, дБ'
            name="АМ/АМ"            
        if name_measure=="pos":
            x_name='Pвх, дБ'
            y_name='Pвых, дБ'
            name="Точка насыщения"
        give_data=norm_data(id_data,name_measure)#Получаем данные(x;y)
        create_svg=plot_graf_in_svg(x_name, y_name,give_data,name)               #Создаем на основе полученных данных график svg
        base_pdf=cr_PDF()                                             #Создаем базовый pdf c таблицами и добавляем туда нужные данные
        base_pdf.common(base_pdf)
        base_pdf.save_file()
        return redirect('ssi_detail',name_ssi)






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