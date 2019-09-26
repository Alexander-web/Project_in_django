from django import forms
from .models import SSI

class SSIform(forms.ModelForm):
    class Meta:
        model = SSI
        fields = ('name', 'input_frequency','output_frequency','band_frequency','available_meas')

