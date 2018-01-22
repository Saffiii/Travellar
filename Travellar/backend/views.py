from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, QueryDict


def fbuser(request):
    return JsonResponse({"success": 'Hello world', "error": False}, safe=False)