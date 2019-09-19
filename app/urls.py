from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('',views.view_list, name='view_list'),
    path('', Baselist.as_view(), name = 'base_list'),
    path('get/', SSIList.as_view(), name = 'ssi_list'),
    path("get/ssi_detail/<slug:ssi>/", SSIDetail.as_view(), name="ssi_detail"),
    path('get/measure/<slug:ssi_name>/<slug:meas_name>/', MeasuresData.as_view(), name="name_meas"),
    path('get/remove/<slug:name_remove>/', Remove_from_que.as_view(), name = 'ssi_remove'),
    path('get/make_measures/', Make_measures.as_view(), name = 'make_measures'),
    
]
    