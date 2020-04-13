from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from .models import Camera, School, CameraModel
import requests
from requests.auth import HTTPBasicAuth


# Create your views here.
def index(request):
    return render(request, 'camera_index.html', {
        "page_title": "Index View"
    })


class CameraCreate(LoginRequiredMixin, CreateView):
    model = Camera
    fields = ['school', 'room', 'model', 'ip_address']
    template_name = 'base_create_page.html'

class SchoolCreate(LoginRequiredMixin, CreateView):
    model = School
    fields = ['name', 'technician']
    template_name = 'base_create_page.html'

class SchoolDetail(LoginRequiredMixin, DetailView):
    model = School
    template_name = 'school_detail.html'

class CameraModelCreate(LoginRequiredMixin, CreateView):
    model = CameraModel
    template_name = 'base_create_page.html'

@login_required
def cameradetail(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    return render(request,
                  'camera_detail.html',
                  {
                      "camera": camera
                  })


@login_required()
def camera_list(request):
    user = request.user
    schools = user.schools.filter(technician_id=user.id)
    return render(request, 'camera_list.html', {
        "Schools": schools
    })
@login_required()
def camera_image(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    r = requests.get(f"http://{camera.ip_address}{camera.model.closeCommand}{camera.model.getCameraUrl}",
                     auth=HTTPBasicAuth(camera.username, camera.password),
                     stream=True)
    if (r.status_code == 200):
        pass
    else:
        return HttpResponseServerError(status=500)


@login_required
def school_list(request):
    schools = School.objects.all()
    return render(request, 'camera_school_list.html', {"Schools": schools})


