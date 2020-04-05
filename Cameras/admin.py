from django.contrib import admin
from .models import School, CameraModel, Camera
# Register your models here.

admin.site.register(School)
admin.site.register(Camera)
admin.site.register(CameraModel)