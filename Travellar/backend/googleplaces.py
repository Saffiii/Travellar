import random
from decimal import Decimal

from googleplaces import GooglePlaces

from .forms import DestinationForm, RatingForm
from .models import Destination, Rating


def initiateGooglePlaces():
    client = GooglePlaces("AIzaSyBFFVsew4wZLKSJF8wjjoPEqFy-MkIewHo")
    text = "popular places in england"

    query_result = client.text_search(text)
    for i in range(3):
        for place in query_result.places:
            place.get_details()
            location = place.details
            loadDestinations(location)
            loadRatings(place, location['place_id'])

        if query_result.next_page_token and len(query_result.next_page_token) > 0:
            token = query_result.next_page_token
            query_result = client.text_search(text, pagetoken=token)


def loadDestinations(location):
    destinationName = location['name']
    destinationType = location['types']
    destinationDescription = "N/A"
    destinationCountry = ""
    destinationState = ""
    destinationAddress = location['formatted_address']
    destinationPlaceID = location['place_id']

    for key in location['address_components']:
        if 'country' in key['types']:
            destinationCountry = key['long_name']

        if 'administrative_area_level_1' in key['types']:
            destinationState = key['long_name']

    if len(location['types']) == 1:
        destinationDescription = destinationName + " can be described as a " + location['types'][0] + " found in " + destinationState
    if len(location['types']) == 2:
        destinationDescription = destinationName + " can be described as a " + location['types'][0] + " and a " + location['types'][1] + " found in " + destinationState
    if len(location['types']) > 2:
        destinationDescription = destinationName + " can be described as a " + location['types'][0] + ", " + location['types'][1] + " and a " +location['types'][2] + " found in " + destinationState

    destinationDict = {
        "destinationName": destinationName,
        "destinationType": destinationType,
        "destinationDescription": destinationDescription,
        "destinationCountry": destinationCountry,
        "destinationState": destinationState,
        "destinationAddress": destinationAddress,
        "destinationPlaceID": destinationPlaceID
    }

    place_exists = Destination.objects.filter(destinationPlaceID=destinationPlaceID).first()
    if place_exists is None:
        if destinationDict is not False:
            destination_form = DestinationForm(destinationDict)
            if destination_form.is_valid():
                destination_form.save()
            else:
                print(destination_form.errors.items())
    else:
        place_exists.destinationName = destinationName
        place_exists.destinationType = destinationType
        place_exists.destinationDescription = destinationDescription
        place_exists.destinationCountry = destinationCountry
        place_exists.destinationState = destinationState
        place_exists.destinationAddress = destinationAddress
        place_exists.save()


def loadRatings(place, GPID):
    destination_exists = Destination.objects.filter(destinationPlaceID=GPID).first()
    if destination_exists:
        d = Destination.objects.get(destinationPlaceID=GPID)
        destinationID = d.destinationID
        rating = place.rating

        if not isinstance(rating, str):
            if rating < 4.1:
                a = random.uniform(0, 1)
                round_a = round(a, 1)
                rating += Decimal.from_float(round_a)
            elif rating > 4.1 and rating < 4.5:
                a = random.uniform(0, 0.5)
                rating += Decimal.from_float(a)
                rating = round(rating, 1)

            if rating > 5.0:
                rating = 5.0

        user = random.randint(3, 94)
        ratingDict = {
            "userID": user,
            "destinationID": destinationID,
            "rating": rating,
        }
        rating_exists = Rating.objects.filter(destinationID_id=destinationID, userID_id=user).first()

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
