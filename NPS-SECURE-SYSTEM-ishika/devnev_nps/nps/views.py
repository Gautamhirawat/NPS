from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nps.urls')),
]

def home(request):
    return render(request, 'nps/home.html')
