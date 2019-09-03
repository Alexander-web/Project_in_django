from django.contrib import admin
from django.utils import timezone
from .models import SSI,MeasureType,MeasureResult,MeasureData

admin.site.register(SSI)
admin.site.register(MeasureType)
admin.site.register(MeasureResult)
admin.site.register(MeasureData)


# admin.site.register(Genre)
# admin.site.register(Publish)
# admin.site.register(Book)

