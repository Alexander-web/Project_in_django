from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('',views.view_list, name='view_list'),
    path('', Baselist.as_view(), name = 'base_list'),
    path('help/', Helplist.as_view(), name = 'help_list'),
    path('get/', SSIList.as_view(), name = 'ssi_list'),
    path("get/ssi_detail/<slug:ssi>/", SSIDetail.as_view(), name="ssi_detail"),
    path('get/measure/<slug:meas_name>/<slug:ssi_name>/', MeasuresData.as_view(), name="name_meas"),
    path('get/remove_from_que/<slug:name_remove>/', Remove_from_que.as_view(), name = 'ssi_remove'),
    path('get/remove_from_measure/<slug:name>/', Remove_from_measure.as_view(), name = 'measure_remove'),
    path('get/make_measures/', views.make_measures, name = 'make_measures'),
    path('get/meastype_info/<slug:mt_name>/<slug:ssi_info_name>/<slug:id_measure>/', Meas_info.as_view(), name = 'meas_info'),
    path('create_SSI', views.ssi_new, name = 'create'),
    path('remove_from_ssilist/<slug:id_name>/', Remove_from_ssilist.as_view(), name = 'ssi_remove_ssilist'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('get/filter/',views.freq_sort, name='filter'),
    path('get/graph/<slug:data_id>/<slug:mt_name>/', Meas_graph.as_view(), name = 'graph'),
    path('get/meastype_info/<slug:mt_name>/<slug:ssi_info_name>/<slug:id_measure>/<slug:valid>/',Check_valid.as_view(), name = 'valid'),
    path('get/key/',views.key_create, name='key'),
    path('get/cr_measure/',views.create_measure, name='create_measure'),
    path('operator/',views.create_operator, name='op'),
    path('payload/',views.create_payload, name='pay_load'),
    path('key_list/', Keys_lists.as_view(), name = 'keys_list'),

]

