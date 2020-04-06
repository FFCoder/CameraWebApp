from django.shortcuts import render, HttpResponse
from .models import Camera


# Create your views here.
def index(request):
    return render(request, 'camera_index.html', {
        "page_title": "Index View"
    })


def cameradetail(request, id):
    camera = Camera.objects.get(id=id)
    return render(request,
                  'camera_detail.html',
                  {
                      "camera": camera
                  })
