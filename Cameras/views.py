from django.shortcuts import render, HttpResponse
from .models import  Camera

# Create your views here.
def Index(request):
    return HttpResponse('Camera View')

def CameraDetail(request, id):
    camera = Camera.objects.get(id=id)
    return render(request,
                  'camera_detail.html',
                  {
                      "camera": camera
                  })