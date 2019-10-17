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
    path('get/make_measures/', Make_measures.as_view(), name = 'make_measures'),
    path('get/meastype_info/<slug:mt_name>/<slug:ssi_info_name>/<slug:id_measure>/', Meas_info.as_view(), name = 'meas_info'),
    path('create_SSI', views.ssi_new, name = 'create'),
    path('remove_from_ssilist/<slug:id_name>/', Remove_from_ssilist.as_view(), name = 'ssi_remove_ssilist'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('get/filter/',views.freq_sort, name='filter'),
    path('get/graph/<slug:id_data>/<slug:meas_type>/', Meas_graph.as_view(), name = 'graph'),
    path('get/make_graph/',views.make_graph, name = 'm_graph'),

]

