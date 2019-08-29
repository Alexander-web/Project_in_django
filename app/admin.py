from django.contrib import admin
from django.utils import timezone
from .models import Genre,Publish,Book

admin.site.register(Genre)
admin.site.register(Publish)
admin.site.register(Book)

