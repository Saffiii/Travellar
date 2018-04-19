import json, sys, os
import requests
import base64
import random
from .forms import AirportForm, HotelForm, VehicleRentalForm
from .models import Airport, Hotel, VehicleRental


def initsabre():
    clientID = 'V1:mvmk0zm2lm812b5z:DEVCENTER:EXT'
    password = 'lE9jNG9m'

    auth_url = 'https://api.test.sabre.com/v1/auth/token'
    sabre_url = 'https://api.test.sabre.com'

    # auth_url = 'https://api-crt.cert.havail.sabre.com/v2/auth/token'
    # sabre_url = 'https://api-crt.cert.havail.sabre.com/v1/lists/top/destinations?origin=NYC&lookbackweeks=8&topdestinations=5'

    access_token = ''

    # Determine user access token or assign standard test if not specified
    if not access_token:
        response = request_authentication(clientID, password, auth_url, sabre_url)
        # else:
        #     access_token = 'T1RLAQKgmcM8BS5uQLhlNAKJ/GIukDsUURDTcJkac2yBZTJP5wW/grIjAADAjwh0RG93FIABjyhF1OEFVWHigSB/xBkl73hb5eQj1LgSaQhwVjNc/7pd+J8i2rHI9uRZFj/4pLhZDIMSUdvOQJHisF5lr3DUUS0tPppf9QKtDWEoU4cze+gkzpEnITMQJ8vgcRPfq/0b1Z2l0LHyWV0yoIUQXGSWE751/jEbn/8yXQNM8gvagpA9JSSqIBDEI4miMHwtIGLX5vcZ3EuvB++VtF+Gj2aQBgMg6bym2B1xgnbzUpFDjeNj7l2Z8DJ9'

    return response


def request_authentication(clientID, password, auth_url, sabre_url):
    clientIDBase64 = base64.b64encode(clientID.encode()).decode()
    passwordBase64 = base64.b64encode(password.encode()).decode()
    fullencode = clientIDBase64 + ':' + passwordBase64
    base64fullencode = base64.b64encode(fullencode.encode()).decode()

    # Authentication request setup
    headers = {
        'Authorization': 'Basic ' + base64fullencode,
        'Content-Type': 'application/x-www-form-urlencoded',
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=headers).json()

    access_token = response['access_token']

    headers2 = {
        'Authorization': 'Bearer ' + str(access_token)
    }

    topDestination = topDestinations(headers2, sabre_url)
    destinations = destinationFinder(headers2, sabre_url)
    hotels = getHotel()
    rental = getRental()
    # hotels = hotelGeoSearch(headers2, sabre_url)
    topRecommendations = sabreRecommendations(headers2, sabre_url)

    response = {'topDestination': topDestination, 'destinations': destinations, 'topRecommendations': topRecommendations, 'hotels': hotels, 'rentals': rental}
    return response


def topDestinations(header, url):
    url += '/v1/lists/top/destinations?&origin=LHR&lookbackweeks=12&topdestinations=8'
    response = requests.get(url, headers=header).json()
    return response


def sabreRecommendations(header, url):
    url += '/v1/lists/top/destinations?&origin=LHR&lookbackweeks=12&topdestinations=50'
    response = requests.get(url, headers=header).json()
    return response


def destinationFinder(header, url):
    url += '/v2/shop/flights/fares?&origin=LHR&lengthofstay=5&topdestinations=10'
    response = requests.get(url, headers=header).json()
    destinationSet = set()
    response2 = dict()
    for counter, key in enumerate(response['FareInfo']):
        if key['DestinationLocation'] not in destinationSet:
            destinationSet.add(key['DestinationLocation'])

            replaceiata = Airport.objects.filter(iata=response['FareInfo'][counter]['DestinationLocation']).first()
            if replaceiata is not None:
                response['FareInfo'][counter]['DestinationLocation'] = replaceiata.city
            response2[counter] = (response['FareInfo'][counter])
            # try:
            #     # os.getcwd() = C:\Users\idree\Desktop\Travellar\Travellar
            #     dir = os.getcwd() + "\\backend\\fixtures\\"
            #     # data = json.load(open(dir + 'airports.json'))
            # except Exception as e:
            #     print(e)

    # for counter, val in enumerate(data):
    # dataDict = {
    #     "icao": data[val]['icao'],
    #     "iata": data[val]['iata'],
    #     "name": data[val]['name'],
    #     "city": data[val]['city'],
    #     "state": data[val]['state'],
    #     "country": data[val]['country'],
    # }
    # place_exists = Airport.objects.filter(iata=data[val]['iata']).first()
    # if place_exists is None:
    #     if dataDict is not False:
    #         airports_form = AirportForm(dataDict)
    #         if airports_form.is_valid():
    #             airports_form.save()
    #         else:
    #             print(airports_form.errors.items())
    # else:
    #     place_exists.icao = data[val]['icao']
    #     place_exists.iata = data[val]['iata']
    #     place_exists.name = data[val]['name']
    #     place_exists.city = data[val]['city']
    #     place_exists.state = data[val]['state']
    #     place_exists.country = data[val]['country']
    #     place_exists.save()

    response = response2
    return response


def getHotel():
    response = dict()
    for key in range(8):
        rnumber = random.randint(0, Hotel.objects.count())
        hotel = Hotel.objects.filter(pk=rnumber).first()
        data = {
            "name": hotel.hotelName,
            "city": hotel.hotelCity,
            "country": hotel.hotelCountry,
        }
        response[key] = data
    # print(response)

    return response


def hotelGeoSearch(header, url):
    # header['Content-Type'] = 'application/json'
    # url += '/v1.0.0/lists/utilities/geosearch/locations?mode=geosearch'
    # data = {
    #     "GeoSearchRQ": {
    #         "version": "1",
    #         "GeoRef": {
    #             "Radius": 200,
    #             "MaxResults": 2,
    #             "UOM": "MI",
    #             "Category": "HOTEL",
    #             "AddressRef": {
    #                 "CountryCode": "GB"
    #             }
    #
    #         }
    #     }
    # }
    #
    # response = requests.post(url, data=data, headers=header).json()
    # print(response)
    # return response

    # try:
    #     # os.getcwd() = C:\Users\idree\Desktop\Travellar\Travellar
    #     dir = os.getcwd() + "\\backend\\fixtures\\"
    #     data = json.load(open(dir + 'hotels.json'))
    # except Exception as e:
    #     print(e)
    # data = data['GeoSearchRS']['GeoSearchResults']['GeoSearchResult']
    # for counter, val in enumerate(data):
    #     if 'Zip' in val:
    #         zip = val['Zip']
    #     else:
    #         zip = "N/A"
    #
    #     if 'Street' in val:
    #         val['Street'] = val['Street']
    #     else:
    #         val['Street'] = "N/A"
    #
    #     dataDict = {
    #         "hotelName": val['Name'],
    #         "hotelStreet": val['Street'],
    #         "hotelZip": zip,
    #         "hotelCity": val['City'],
    #         "hotelCountry": val['Country'],
    #         "hotelSabreID": val['Id'],
    #     }
    #
    #     hotel_exists = Hotel.objects.filter(hotelSabreID=val['Id']).first()
    #     if hotel_exists is None:
    #         if dataDict is not False:
    #             hotel_form = HotelForm(dataDict)
    #             if hotel_form.is_valid():
    #                 hotel_form.save()
    #             else:
    #                 print(hotel_form.errors.items())
    #     else:
    #         hotel_exists.hotelName = val['Name']
    #         hotel_exists.hotelStreet = val['Street']
    #         hotel_exists.hotelZip = zip
    #         hotel_exists.hotelCity = val['City']
    #         hotel_exists.hotelCountry = val['Country']
    #         hotel_exists.hotelSabreID = val['Id']
    #         hotel_exists.save()
    #     print(dataDict)
    return


def getRental():
    # try:
    #     # os.getcwd() = C:\Users\idree\Desktop\Travellar\Travellar
    #     dir = os.getcwd() + "\\backend\\fixtures\\"
    #     data = json.load(open(dir + 'rental.json'))
    # except Exception as e:
    #     print(e)
    # data = data['GeoSearchRS']['GeoSearchResults']['GeoSearchResult']
    # for counter, val in enumerate(data):
    #     if 'Zip' in val:
    #         zip = val['Zip']
    #     else:
    #         zip = "N/A"
    #
    #     if 'Street' in val:
    #         val['Street'] = val['Street']
    #     else:
    #         val['Street'] = "N/A"
    #
    #     if any(char.isdigit() for char in val['Name']) and ' ' in val['Name']:
    #         val['Name'] = (val['Name'].split(' ', 1)[1])
    #
    #
    #
    #     dataDict = {
    #         "vehicleCompany": val['Name'],
    #         "vehicleStreet": val['Street'],
    #         "vehicleZip": zip,
    #         "vehicleCity": val['City'],
    #         "vehicleCountry": val['Country'],
    #         "vehicleSabreID": val['Id'],
    #     }
    #
    #     print(val['Name'])
    #     rental_exists = VehicleRental.objects.filter(vehicleSabreID=val['Id']).first()
    #     if rental_exists is None:
    #         if dataDict is not False:
    #             vehicle_form = VehicleRentalForm(dataDict)
    #             if vehicle_form.is_valid():
    #                 vehicle_form.save()
    #             else:
    #                 print(vehicle_form.errors.items())
    #     else:
    #         rental_exists.vehicleCompany = val['Name']
    #         rental_exists.vehicleStreet = val['Street']
    #         rental_exists.vehicleZip = zip
    #         rental_exists.vehicleCity = val['City']
    #         rental_exists.vehicleCountry = val['Country']
    #         rental_exists.vehicleSabreID = val['Id']
    #         rental_exists.save()
    #     # print(dataDict)

    response = dict()
    for key in range(8):
        rnumber = random.randint(0, VehicleRental.objects.count())
        rental = VehicleRental.objects.filter(pk=rnumber).first()
        company = ''
        city = ''
        country = ''
        if rental is not None:
            if rental.vehicleCompany is not None:
                company = rental.vehicleCompany
            if rental.vehicleCity:
                city = rental.vehicleCity
            if rental.vehicleCountry:
                country = rental.vehicleCountry

        data = {
            "company": company,
            "city": city,
            "country": country,
        }
        response[key] = data
    # print(response)

    return response
