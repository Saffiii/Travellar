from django.db import models

# Using ORM models, Django uses these models to create database migrations


class Destination(models.Model):
    destinationID = models.AutoField(primary_key=True)
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

    def as_json(self):
        return dict(
            destinationID=self.destinationID,
            destinationName=self.destinationName,
            destinationType=self.destinationType,
            destinationDescription=self.destinationDescription,
            destinationCountry=self.destinationCountry,
            destinationState=self.destinationState,
            destinationAddress=self.destinationAddress,
            destinationCurrency=self.destinationCurrency,
            destinationMinPrice=self.destinationMinPrice,
            destinationMaxPrice=self.destinationMaxPrice,
            destinationMinTemp=self.destinationMinTemp,
            destinationMaxTemp=self.destinationMaxTemp,
        )


class Hotel(models.Model):
    hotelID = models.AutoField(primary_key=True)
    hotelName = models.CharField(max_length=255)
    hotelLocation = models.CharField(max_length=255)
    hotelContact = models.IntegerField()
    hotelCheckin = models.DateField(auto_now_add=True)
    hotelCheckout = models.DateField(auto_now_add=True)
    hotelDescription = models.CharField(max_length=255)
    hotelImage = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=255)
    hotelPrice = models.DecimalField(decimal_places=2, max_digits=10)

    def as_json(self):
        return dict(
            hotelID=self.hotelID,
            hotelName=self.hotelName,
            hotelLocation=self.hotelLocation,
            hotelContact=self.hotelContact,
            hotelCheckin=self.hotelCheckin,
            hotelCheckout=self.hotelCheckout,
            hotelDescription=self.hotelDescription,
            hotelImage=self.hotelImage,
            hotelPrice=self.hotelPrice,
        )


class VehicleRental(models.Model):
    vehicleID = models.AutoField(primary_key=True)
    vehicleCompany = models.CharField(max_length=255)
    vehicleLocation = models.CharField(max_length=255)
    vehicleType = models.CharField(max_length=255)
    vehicleRate = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleMileageAllowance = models.IntegerField()
    vehicleBaseCost = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleTotalCost = models.DecimalField(decimal_places=2, max_digits=10)
    vehicleCurrency = models.CharField(max_length=25)

    def as_json(self):
        return dict(
            vehicleID=self.vehicleID,
            vehicleCompany=self.vehicleCompany,
            vehicleLocation=self.vehicleLocation,
            vehicleType=self.vehicleType,
            vehicleRate=self.vehicleRate,
            vehicleMileageAllowance=self.vehicleMileageAllowance,
            vehicleBaseCost=self.vehicleBaseCost,
            vehicleTotalCost=self.vehicleTotalCost,
            vehicleCurrency=self.vehicleCurrency,
        )


class User(models.Model):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)
    # password =
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)

    def as_json(self):
        return dict(
            userID=self.userID,
            first_name=self.firstName,
            last_name=self.lastName,
            email=self.email,
        )


class History(models.Model):
    userID = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    destinationID = models.ForeignKey(
        'Destination',
        on_delete=models.CASCADE,
    )

    def as_json(self):
        return dict(
            userID=self.userID,
            destinationID=self.destinationID,
        )


class ReviewDestination(models.Model):
    destinationID = models.ForeignKey(
        'Destination',
        on_delete=models.CASCADE,
    )
    review = models.TextField(max_length=10000)

    def as_json(self):
        return dict(
            destinationID=self.destinationID,
            review=self.review
        )


class ReviewHotel(models.Model):
    hotelID = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE,
    )
    review = models.TextField(max_length=10000)

    def as_json(self):
        return dict(
            hotelID=self.hotelID,
            review=self.review
        )


class ReviewVehicleRental(models.Model):
    vehicleID = models.ForeignKey(
        'VehicleRental',
        on_delete=models.CASCADE,
    )
    review = models.TextField(max_length=10000)

    def as_json(self):
        return dict(
            vehicleID=self.vehicleID,
            review=self.review
        )


class StarredDestination(models.Model):
    userID = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    destinationID = models.ForeignKey(
        'Destination',
        on_delete=models.CASCADE,
    )
    starred = models.BooleanField()

    def as_json(self):
        return dict(
            userID=self.userID,
            destinationID=self.destinationID,
            starred=self.starred
        )


class StarredHotel(models.Model):
    userID = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    hotelID = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE,
    )
    starred = models.BooleanField()

    def as_json(self):
        return dict(
            userID=self.userID,
            hotelID=self.hotelID,
            starred=self.starred
        )


class StarredVehicleRental(models.Model):
    userID = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    vehicleID = models.ForeignKey(
        'VehicleRental',
        on_delete=models.CASCADE,
    )
    starred = models.BooleanField()

    def as_json(self):
        return dict(
            userID=self.userID,
            vehicleID=self.vehicleID,
            starred=self.starred
        )


class Ratings(models.Model):
    #userID=models.IntegerField()
    destinationID = models.ForeignKey(
        'Destination',
        on_delete=models.CASCADE,
    )
    rating = models.FloatField()
    timestamp = models.TimeField
