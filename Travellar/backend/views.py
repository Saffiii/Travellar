from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, QueryDict
from .googleplaces import initiateGooglePlaces
from .localrecommender import initLocalRecommenderPearson
from .localrecommenderals import initLocalRecommenderALS
from .sabre import initsabre
import json
from .forms import DestinationForm, RatingForm, UserForm
from .models import Destination, Rating, User


def fbuser(request):
    return JsonResponse({"success": 'Facebook', "error": False}, safe=False)


def googleplaces(request):
    initiateGooglePlaces()
    return JsonResponse({"success": 'Google', "error": False}, safe=False)


def recommend(request):
    initLocalRecommenderPearson()
    return JsonResponse({"success": 'recommendation_pearson', "error": False}, safe=False)


def recommendals(request):
    print('###########ALS###########')

    if request.method == 'POST':
        data = json.loads(request.body)
        placedata = data['place']
        email = data['email']
        username = data['name']
        rating = 5
        firstname = username.split(' ', 1)[0]
        lastname = username.split(' ', 1)[1]

        user_exists = User.objects.filter(email=email).first()
        userDict = {
            "email": email,
            "firstName": firstname,
            "lastName": lastname
        }
        if user_exists is None:
            if userDict is not False:
                user_form = UserForm(userDict)
                if user_form.is_valid():
                    user_form.save()
                else:
                    print(user_form.errors.items())

        for key in placedata:
            locationcity = 'N/A'
            locationcountry = 'N/A'
            locationstreet = 'N/A'
            locationid = key['place']['id']
            locationname = key['place']['name']
            locationtype = 'Holiday'

            if 'street' in key['place']['location']:
                locationstreet = key['place']['location']['street']
            if 'country' in key['place']['location']:
                locationcountry = key['place']['location']['country']
            if 'city' in key['place']['location']:
                locationcity = key['place']['location']['city']

            locationdescription = locationname + " can be described as a point of establishment found in " + locationcity
            locationcity = locationcity.split(',', 1)[0]

            destinationDict = {
                "destinationName": locationname,
                "destinationType": locationtype,
                "destinationDescription": locationdescription,
                "destinationCountry": locationcountry,
                "destinationState": locationcity,
                "destinationAddress": locationstreet,
                "destinationPlaceID": locationid
            }

            destination_exists = Destination.objects.filter(destinationPlaceID=locationid).first()
            if destination_exists is None:
                if destinationDict is not False:
                    destination_form = DestinationForm(destinationDict)
                    if destination_form.is_valid():
                        destination_form.save()
                    else:
                        print(destination_form.errors.items())
            else:
                destination_exists.destinationName = locationname
                destination_exists.destinationType = locationtype
                destination_exists.destinationDescription = locationdescription
                destination_exists.destinationCountry = locationcountry
                destination_exists.destinationState = locationcity
                destination_exists.destinationAddress = locationstreet
                destination_exists.save()

            ratingDict = {
                "userID": user_exists.pk,
                "destinationID": destination_exists.pk,
                "rating": rating,
            }

            rating_exists = Rating.objects.filter(destinationID_id=destination_exists.pk, userID_id=user_exists.pk).first()
            if rating_exists is None:
                if ratingDict is not False:
                    rating_form = RatingForm(ratingDict)
                    if rating_form.is_valid():
                        rating_form.save()
                    else:
                        print(rating_form.errors.items())
            else:
                rating_exists.rating = rating
                rating_exists.save()

    # return JsonResponse({"success": 'ALS', "error": False}, safe=False)

    recommendations = []
    for x in range(5):
        result = initLocalRecommenderALS(user_exists.pk)
        recommendations.append(result)
    data_set = (set(recommendations))
    # data_list = list(data_set)
    data_dict = dict.fromkeys(data_set,0)
    data_list = list()
    for key in data_dict:
        destination_info = Destination.objects.filter(destinationName=key).first()
        print(destination_info.destinationName)
        print(destination_info.destinationCountry)
        print(destination_info.destinationState)
        entry = {
            "name": destination_info.destinationName,
            "country": destination_info.destinationCountry,
            "state": destination_info.destinationState
        }
        data_list.append(entry)
    return JsonResponse({"success": 'recommendation_als', "error": False, "data": data_list}, safe=False)


def sabre(request):
    response = initsabre()
    # print(response)
    return JsonResponse({"success": 'sabre', "error": False, "data": response}, safe=False)
