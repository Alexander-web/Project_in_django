from django.shortcuts import render
from .client_server.tcp_client import send_and_return
# from .client_server.tcp_server import create_data
from .models import *
from django.views.generic import TemplateView
from django.http import HttpResponse

    # Представления
# def view_list(request):
#     data=send_and_return('measure_afc')
#     data=data.replace(',', '.')
#     data=data[0:data.__len__()-2]
#     s=data.split(';')
#     s=s[1:]
#     for i in s:
#         xy = i.split(':')
#         x=float(xy[0])
#         y=float(xy[1])
#         MeasureData.objects.create(x=x, y=y)
#     return HttpResponse("Ok")

class Data(TemplateView):
    template_name = 'app/measure.html'
    def get(self,req,name):
        d={}
        data=send_and_return(name)
        data=data.replace(',', '.')
        data=data[0:data.__len__()-2]
        s=data.split(';')
        s=s[1:]
        for i in s:
            xy = i.split(':')
            x=float(xy[0])
            y=float(xy[1])
            MeasureData.objects.create(x=x, y=y)
        score=MeasureData.objects.count()
        context={'name':name,'score':score}
        context['name_meas']=MeasureData.objects.all()
        return render(req, self.template_name,context)

class SSIList(TemplateView):
    template_name = 'app/index.html'
    def get(self,req):
        context={}
        context['ssi'] = SSI.objects.all()
        return render(req, self.template_name,context)

class Baselist(TemplateView):
    template_name = 'app/base.html'
    def get(self,req):
        context={}
        # context['ssi'] = SSI.objects.all()
        return render(req, self.template_name,context)

class SSIDetail(TemplateView):
    template_name = 'app/ssi_detail.html'
    def get(self,req,ssi):
        context={}
        context['ssi'] = SSI.objects.get(name = ssi)
        return render(req, self.template_name,context)


# def get_data(request):
#     data=[]
#     meas=[]
#     d = list(SSI.objects.values('name','meas_type__name'))
#     for i in d:
#         data.append('{} '.format(i['name']))
#         meas.append('изм. {} '.format(i['meas_type__name']))
#     context={
#         "data_name":data,
#         'data_meas':meas
#     }
#     return render(request, 'app/index.html', context)

# def measure_view(request,offset):
#     measure = MeasureData.objects.get(slug=offset)
#     context={
#         "measure": measure,
#     }
#     return render(request, 'app/measure.html', context)

# def get_data(request):
#     meas=[]
#     m={}
#     n={}
#     b=1
#     q = list(SSI.objects.values('name'))
#     f = list(SSI.objects.values('meas_type__name'))
#     f1 =list(SSI.objects.values('meas_type__name','name'))
#     def true_or_false(meas_type__name):
#         for i in f1:
#             if i==meas_type__name:
#                 del f1[0]
#                 return True
#             else:
#                 return False
#     while b<=len(q):
#         for i in q:
#             meas.clear()
#             for j in f:
#                 d={'name': i['name'],'meas_type__name': j['meas_type__name']}
#                 if true_or_false(d) == True:
#                     meas.append(j['meas_type__name'])
#                 else:
#                     pass
#             n={i['name']:list(tuple(meas))}
#             m.update(n)
#             b+=1
#     context={
#         'data':m.keys(),
#         'meas':m.values()
#     }
#     return render(request, 'app/index.html', context)
