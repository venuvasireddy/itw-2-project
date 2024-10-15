from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import loader
def login(request):
  return render(request,'login.html')


def profile(request):
  return render(request,'profile.html')


def approve_resourse(request):
  return render(request,'approve.html')


def course(request):
  return render(request,'course.html')

def home(request):
  return render(request,'home.html')

def addresource(request):
  return render(request,'addresource.html')

