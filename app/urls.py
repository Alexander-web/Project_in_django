from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_list, name='view_list'),
    path('get/',views.get_data, name='get_data')
]
    