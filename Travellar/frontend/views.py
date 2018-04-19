from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse


def index(request):
    return render(request, 'frontend/index.html')


def recommendations(request):
    return render(request, 'frontend/recommendations.html')


def flights(request):
    return render(request, 'frontend/flights.html')


def hotel(request):
    return render(request, 'frontend/hotel.html')


def rental(request):
    return render(request, 'frontend/rental.html')

