from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
import logging
from .models import Car
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
        except:
            pass

def get_dealers_from_cf():
    try:
        # Use the actual URL of your dealer-get service
        dealer_get_service_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/54ee907b-434c-4f03-a1b3-513c235fbeb4/default/myAction'

        # Use your provided IAM API Key in the request header
        headers = {
            'Authorization': 'Bearer Udq3_mK0zxdnBA4cx2bBE045ZYD2BtzGF5tGT20fFKOh',
            'Accept': 'application/json'
        }

        # Make a GET request to the cloud function
        requests.get(dealer_get_service_url, headers=headers)
