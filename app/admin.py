from django.contrib import admin
from django.utils import timezone
from .models import SSI,MeasureType,Measure_que,AcceptData

admin.site.register(SSI)
admin.site.register(MeasureType)
admin.site.register(Measure_que)
admin.site.register(AcceptData)



