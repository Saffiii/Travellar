from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse

def index(request):
    return render(request, 'frontend/index.html')


