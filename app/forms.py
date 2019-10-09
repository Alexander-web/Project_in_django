from django import forms
from .models import SSI
from django.contrib.auth.forms import UserCreationForm

'''
Класс отвечает за создание формы, где model = SSI показывает какой класс будет использоваться для создания формы,
fields говорит, какие поля использовать для этого.
'''

class SSIform(forms.ModelForm):
    class Meta:
        model = SSI
        fields = ('name', 'input_frequency','output_frequency','band_frequency','available_meas',)

class Formfilter(forms.Form):
    choice=forms.CharField(widget=forms.Select())
