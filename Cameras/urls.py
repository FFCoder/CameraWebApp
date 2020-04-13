from django.urls import path
from . import views
app_name = 'cameras'
urlpatterns = [
    path('', views.index, name='index'),
    path('cameras/', views.camera_list, name='camera_list'),
    path('cameras/create/', views.CameraCreate.as_view(), name='camera_create'),
    path('cameras/<int:camera_id>', views.cameradetail, name='camera_detail'),
    path('schools/', views.school_list, name='school_list'),
    path('schools/<int:pk>',views.SchoolDetail.as_view(), name='school_detail'),
    path('schools/create/', views.SchoolCreate.as_view(), name='school_create'),
    path('models/create/', views.CameraCreate.as_view(), name='model_create')


]