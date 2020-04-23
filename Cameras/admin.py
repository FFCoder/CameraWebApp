from django.contrib import admin
from .models import School, CameraModel, Camera
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from requests import ConnectTimeout
# Register your models here.

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "technician")
    readonly_fields = ("show_url",)
    def show_url(self, instance):
        url = reverse('cameras:school_detail', kwargs={"pk": instance.pk})
        response = """<a href="{0}">{0}</a>""".format(url)
        return mark_safe(response)
    show_url.short_description = "School Url"

class CameraAdmin(admin.ModelAdmin):
    actions = ['open']
    #actions = None

    def open(self, request, queryset):
        for cam in queryset.all():
            try:
                cam.open()
            except ConnectTimeout:
                messages.add_message(request, messages.ERROR, f"Connection Timeout while attempting to open {cam}")
    open.short_description = 'Open Cameras'


admin.site.register(School, SchoolAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraModel)
admin.site.index_title = "GSCS Cameras"
admin.site.site_header = 'Cameras Admin'
admin.site.site_title = "Cameras Admin"