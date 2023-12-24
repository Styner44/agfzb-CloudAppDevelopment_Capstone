"""
This module handles the views for the car dealership application.
"""

import json
from datetime import datetime
import logging
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Car
from .restapis import get_dealers_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)

def add_review(request, dealer_id):
    """
    Add a review for a car dealer.
    """
    if request.method == 'GET':
        cars = Car.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', {'cars': cars, 'dealer_id': dealer_id})

    if request.method == 'POST':
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

            json_payload = {"review": review}

            # The Cloudant service URL for posting the review to the database
            cloudant_service_url = (
                "https://41b72835-e355-48ae-9d54-2ba6dc3c140e-bluemix."
                "cloudantnosqldb.appdomain.cloud"
            )

            # Use your provided IAM API Key in the request header
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer Udq3_mK0zxdnBA4cx2bBE045ZYD2BtzGF5tGT20fFKOh',
            }

            # Make a POST request to the Cloudant server with json_payload
            response = requests.post(
                cloudant_service_url,
                json=json_payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                return redirect('djangoapp:dealer_details', dealer_id=dealer_id)

            return HttpResponse(
                f'Failed to post review. Status code: {response.status_code}',
                status=response.status_code
            )
        except Car.DoesNotExist:
            return HttpResponseBadRequest('Invalid car ID')
        except ValueError:
            return HttpResponseBadRequest('Invalid date format')
        except requests.RequestException as e:
            logger.error("Error posting review to Cloudant: %s", str(e))
            return HttpResponse('Failed to post review to Cloudant', status=500)

    return HttpResponseNotAllowed('Invalid HTTP method')

def get_dealerships(request):
    """
    Get a list of car dealerships. Returns JSON data by default.
    If a query parameter 'names_only' is set to 'true', returns a space-separated string of dealer short names.
    """
    if request.method == 'GET':
        # Call get_dealers_from_cf from restapis.py
        dealer_get_service_url = (
            'https://us-south.functions.appdomain.cloud/api/v1/web/54ee907b-434c-4f03-a1b3-513c235fbeb4/default/myAction'
        )
        dealers = get_dealers_from_cf(dealer_get_service_url)

        # Check if 'names_only' query parameter is set to 'true'
        if request.GET.get('names_only', '').lower() == 'true':
            # Extract short names of dealers and return as a space-separated string
            dealer_names = ' '.join([dealer['short_name'] for dealer in dealers])
            return HttpResponse(dealer_names)

        # Create a list of dealership data and return as JSON
        dealerships_data = [
            {
                'address': dealer.address,
                'city': dealer.city,
                'full_name': dealer.full_name,
                'id': dealer.id,
                'lat': dealer.lat,
                'long': dealer.long,
                'short_name': dealer.short_name,
                'st': dealer.st,
                'zip': dealer.zip
            } for dealer in dealers
        ]
        return HttpResponse(json.dumps(dealerships_data), content_type='application/json')

    return HttpResponseNotAllowed('Invalid HTTP method')

def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        # Call the review-get service
        review_get_service_url = f"your-cloud-function-domain/reviews/review-get?dealerId={dealer_id}"
        dealer_reviews = get_dealer_reviews_from_cf(review_get_service_url, dealer_id)

        # Process each review
        for review in dealer_reviews:
            review.sentiment = analyze_review_sentiments(review.review)

        # Render a template with reviews
        context = {'dealer_id': dealer_id, 'dealer_reviews': dealer_reviews}
        return render(request, 'djangoapp/dealer_details.html', context)
