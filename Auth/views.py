from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from Cameras.models import School


# Create your views here.

def profile(request):
    user = request.user
    schools = School.objects.filter(technician_id=user.id)
    return render(request, 'auth_profile.html', {"User": user, "Schools": schools}) if user.is_authenticated else redirect('login')