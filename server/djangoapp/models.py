# Other model classes...from django.db import models
from django.utils.timezone import now
from django.db import models

# Car Make model with fields: Name, Description, Country, Founded Date, etc.
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=now)
    country = models.CharField(max_length=255)
    founded_date = models.DateField()

    def __str__(self):
        return self.name

# Car Model model with fields: Make, Name, Dealer ID, Type, Year, Engine, Price, MPG, etc.
class CarModel(models.Model):
    SEDAN = 'SD'
    SUV = 'SV'
    WAGON = 'WG'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer = models.ForeignKey('CarDealer', on_delete=models.CASCADE)  # Corrected this line
    car_type = models.CharField(
        max_length=2,
        choices=CAR_TYPES,
        default=SEDAN,
    )
    year = models.IntegerField()
    engine = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    mpg = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

# Car Dealer model with fields: Name, City, State, ST
class CarDealer(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    st = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Dealer Review model with fields: Dealership, Name, Purchase, Review, Purchase Date, Car Make, Car Model, Car Year, etc.
class DealerReview(models.Model):
    dealership = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.IntegerField()

    def __str__(self):
        return self.name
