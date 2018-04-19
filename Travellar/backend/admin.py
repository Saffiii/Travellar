from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Destination, Hotel, VehicleRental, User, History, ReviewVehicleRental, ReviewHotel, ReviewDestination, StarredVehicleRental, StarredHotel, StarredDestination, Rating, Airport
# Register your models here.

admin.site.register(Destination)
admin.site.register(Hotel)
admin.site.register(VehicleRental)
admin.site.register(User)
admin.site.register(History)
admin.site.register(ReviewDestination)
admin.site.register(ReviewHotel)
admin.site.register(ReviewVehicleRental)
admin.site.register(StarredDestination)
admin.site.register(StarredHotel)
admin.site.register(StarredVehicleRental)
admin.site.register(Airport)


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)


admin.site.register(Rating, RatingAdmin)
