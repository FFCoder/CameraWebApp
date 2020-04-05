from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('<int:id>', views.CameraDetail, name='camera_detail')
]