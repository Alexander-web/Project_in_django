from django import forms
from .models import SSI,Operator,SpaceCraft,PayLoad,Keys,MeasureType
from django.contrib.auth.forms import UserCreationForm

'''
Класс отвечает за создание формы, где model = SSI показывает какой класс будет использоваться для создания формы,
fields говорит, какие поля использовать для этого.
'''
CHOICES = (
    ('offline', 'Использовать offline сервер'),
    ('real', 'Использовать векторный анализатор цепей'),
)
CHOICES_VALID = (
    ('valid', 'Измерения проведены'),
    ('invalid', 'Измерения отсутствуют'),
    ('not_chosen', 'Не проверено!'),
)

class SSIform(forms.ModelForm):
    class Meta:
        model = SSI
        fields = ('name', 'input_frequency','output_frequency','band_frequency','available_meas', 'pay_load')

class Keysform(forms.ModelForm):
    class Meta:
        model = Keys
        fields = ('namber_of_points_for_smoothing','input_power','input_power_first', 'input_power_last','width_filter','namber_of_points_for_averaging')

class MeasureTypeform(forms.ModelForm):
    class Meta:
        model = MeasureType
        fields = ('name','key')
        widgets = { 'key' : forms.Select(attrs={'size':'1'}) }

class Operatorform(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ('firstname', 'lastname','accept_data')

class SpaceCraftform(forms.ModelForm):
    class Meta:
        model = SpaceCraft
        fields = ('name',)

class PayLoadform(forms.ModelForm):
    class Meta:
        model = PayLoad
        fields = ('name','spacecraft')

class Formfilter(forms.Form):
    choice=forms.CharField(widget=forms.Select())

class Choose_device(forms.Form):
    choose=forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES, initial='real')

# class UploadFileForm(forms.Form):
#     file = forms.FileField()

# class Valid_maesures(forms.Form):
#     valid=forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES_VALID, initial='not_chosen')
