from django.shortcuts import render, get_object_or_404, redirect
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest
import logging
from .models import CarModel, Dealer, DealerReview, Car
import requests
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

def add_review(request, dealer_id):
    if request.method == 'GET':
        cars = Car.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', {'cars': cars, 'dealer_id': dealer_id})

    elif request.method == 'POST':
        try:
            # Validate the presence of required fields in the POST data
            purchase_check = request.POST.get('purchasecheck')
            content = request.POST.get('content')
            purchasedate = request.POST.get('purchasedate')
            car_id = request.POST.get('car')

            if not (purchase_check and content and purchasedate and car_id):
                return HttpResponseBadRequest('Invalid or missing POST data')

            # Convert purchasedate to ISO format
            purchase_date = datetime.strptime(purchasedate, '%m/%d/%Y').isoformat()

            car = Car.objects.get(id=car_id)

            review = {
                'dealership': dealer_id,
                'name': request.user.username,
                'purchase': purchase_check,
                'review': content,
                'purchase_date': purchase_date,
                'car_make': car.make.name,
                'car_model': car.name,
                'car_year': car.year.year,
            }

            json_payload = {
                "review": review
            }

            # Make a POST request to the Cloudant server with json_payload
            # Replace 'cloudant_server' with your actual Cloudant server URL
            response = requests.post('cloudant_server', json=json_payload)

            if response.status_code == 200:
                return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
            else:
                return HttpResponse(f'Failed to post review. Status code: {response.status_code}', status=response.status_code)

        except Car.DoesNotExist:
            return HttpResponseBadRequest('Invalid car ID')
        except ValueError:
            return HttpResponseBadRequest('Invalid date format')
        except requests.RequestException as e:
            logger.error(f"Error posting review to Cloudant: {str(e)}")
            return HttpResponse('Failed to post review to Cloudant', status=500)
