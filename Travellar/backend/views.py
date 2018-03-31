from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, QueryDict
from .googleplaces import initiateGooglePlaces
from .localrecommender import initLocalRecommenderPearson
from .localrecommenderals import initLocalRecommenderALS


def fbuser(request):
    return JsonResponse({"success": 'Facebook', "error": False}, safe=False)


def googleplaces(request):
    initiateGooglePlaces()
    return JsonResponse({"success": 'Google', "error": False}, safe=False)


def recommend(request):
    initLocalRecommenderPearson()
    return JsonResponse({"success": 'recommendation_pearson', "error": False}, safe=False)


def recommendals(request):
    recommendations = []
    for x in range(5):
        result = initLocalRecommenderALS()
        recommendations.append(result)
    print(set(recommendations))
    return JsonResponse({"success": 'recommendation_als', "error": False}, safe=False)
