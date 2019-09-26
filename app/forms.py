from django import forms
from .models import SSI,MeasureType

TYPE_CHOICES = (
    ('1', 'afc'),
    ('2', 'pos'),
    ('3', 'amam'),
    ('4', 'gd'),
)
class SSIform(forms.ModelForm):
    class Meta:
        model = SSI
        fields = ('name', 'input_frequency','output_frequency','band_frequency','available_meas')

class Typeform(forms.ModelForm):
    class Meta:
        model = MeasureType
        fields = ('name',)