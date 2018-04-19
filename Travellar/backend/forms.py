from .models import Destination, Hotel, VehicleRental, User, History, ReviewDestination, ReviewHotel, ReviewVehicleRental, StarredDestination, StarredHotel, StarredVehicleRental, Rating, Airport
from django.forms import ModelForm
from django import forms


class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class VehicleRentalForm(ModelForm):
    class Meta:
        model = VehicleRental
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = '__all__'


class ReviewDestinationForm(ModelForm):
    class Meta:
        model = ReviewDestination
        fields = '__all__'


class ReviewHotelForm(ModelForm):
    class Meta:
        model = ReviewHotel
        fields = '__all__'


class ReviewVehicleRentalForm(ModelForm):
    class Meta:
        model = ReviewVehicleRental
        fields = '__all__'


class StarredDestinationForm(ModelForm):
    class Meta:
        model = StarredDestination
        fields = '__all__'


class StarredHotelForm(ModelForm):
    class Meta:
        model = StarredHotel
        fields = '__all__'


class StarredVehicleRentalForm(ModelForm):
    class Meta:
        model = StarredVehicleRental
        fields = '__all__'


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'


class AirportForm(ModelForm):
    class Meta:
        model = Airport
        fields = ['iata', 'city']
