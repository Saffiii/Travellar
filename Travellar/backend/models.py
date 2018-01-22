from django.db import models

# Using ORM models, Django uses these models to create database migrations


class Destination(models.Model):
    destinationName = models.CharField(max_length=255)
    destinationType = models.CharField(max_length=255)
    destinationDescription = models.CharField(max_length=255)
    destinationCountry = models.CharField(max_length=255)
    destinationState = models.CharField(max_length=255)
    destinationAddress = models.CharField(max_length=255)
    destinationCurrency = models.CharField(max_length=25)
    destinationMinPrice = models.DecimalField(decimal_places=2, max_digits=10)
    destinationMaxPrice = models.DecimalField(decimal_places=2, max_digits=10)
    destinationMinTemp = models.DecimalField(decimal_places=2, max_digits=10)
    destinationMaxTemp = models.DecimalField(decimal_places=2, max_digits=10)


class Hotel(models.Model):
    hotelName = models.CharField(max_length=255)
    hotelLocation = models.CharField(max_length=255)
    hotelContact = models.IntegerField()
    hotelCheckin = models.DateField(auto_now_add=True)
    hotelCheckout = models.DateField(auto_now_add=True)
    hotelDescription = models.CharField(max_length=255)
    # hotelImage = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=255) #download pillow
    hotelPrice = models.DecimalField(decimal_places=2, max_digits=10)


class VehicleRental(models.Model):
    vehicleCompany = models.CharField(max_length=255)
    vehicleLocation = models.CharField(max_length=255)
    vehicleType = models.CharField(max_length=255)
    vehicleRate = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleMilleageAllowance = models.IntegerField()
    vehicleBaseCost = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleTotalCost = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleCurrency = models.CharField(max_length=25)


class User(models.Model):
    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)
    # password =
    firstName = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)

    def as_json(self):
        return dict(
            id=self.id,
            first_name=self.firstName,
            last_name=self.lastname,
            email=self.email,
        )
