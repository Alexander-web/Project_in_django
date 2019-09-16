from django.contrib import admin
from django.utils import timezone
from .models import SSI,MeasureType,Measure,MeasureData

admin.site.register(SSI)
admin.site.register(MeasureType)
admin.site.register(Measure)
admin.site.register(MeasureData)



