from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def site_logout(request):
    logout(request)
    return redirect('cameras:index')