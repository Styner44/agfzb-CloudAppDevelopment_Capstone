from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from djangoapp.models import CarMake, CarModel, Dealership

class DealershipViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')  # replace 'get_dealerships' with 'index'
        Dealership.objects.create(name='Test Dealership', city='Test City', state='Test State', street='Test Street', zip='Test Zip')

    def test_get_dealerships(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Dealership')

class CarMakeModelTest(TestCase):
    def setUp(self):
        self.car_make = CarMake.objects.create(name="Test Make", founded_date=date.today())
        self.car_model = CarModel.objects.create(make=self.car_make, dealer_id=1, name="Test Model", year=2023, price=50000, mpg=30)

    def test_car_make(self):
        self.assertEqual(self.car_make.name, "Test Make")

    def test_car_model(self):
        self.assertEqual(self.car_model.name, "Test Model")
        self.assertEqual(self.car_model.make, self.car_make)
        self.assertEqual(self.car_model.dealer_id, 1)

    def test_multiple_car_models(self):
        car_model1 = CarModel.objects.create(make=self.car_make, dealer_id=1, name="Test Model 1", year=2023, price=50000, mpg=30)
        car_model2 = CarModel.objects.create(make=self.car_make, dealer_id=1, name="Test Model 2", year=2024, price=60000, mpg=35)
    
        self.assertEqual(car_model1.make, self.car_make)
        self.assertEqual(car_model2.make, self.car_make)