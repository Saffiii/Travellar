from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Destination, Hotel, VehicleRental, User
# Register your models here.

admin.site.register(Destination)
admin.site.register(Hotel)
admin.site.register(VehicleRental)
admin.site.register(User)
