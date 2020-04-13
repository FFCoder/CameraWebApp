from django.contrib import admin
from .models import School, CameraModel, Camera
from django.urls import reverse
# Register your models here.

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "technician")
    readonly_fields = ("show_url",)
    def show_url(selfself, instance):
        url = reverse('cameras:school_detail', kwargs={"pk": instance.pk})
        response = """<a href="{0}">{0}</a>""".format(url)
        return response
    show_url.short_description = "School Url"
    show_url.allow_tags = True

admin.site.register(School, SchoolAdmin)
admin.site.register(Camera)
admin.site.register(CameraModel)