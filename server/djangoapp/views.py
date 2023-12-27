"""
This module contains views for adding reviews and getting dealer details in a Django application.
"""

from datetime import datetime
import logging
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from djangoapp.models import CarDealerModel
from djangoapp.models import Car, CarDealerModel  # Added CarDealerModel here

# Logger setup
logger = logging.getLogger(__name__)

def about(request):
    return render(request, 'djangoapp/about.html')

@login_required
def add_review(request, dealer_id):
    """Add a review for a car dealer."""
    if request.method == 'GET':
        cars = Car.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', {'cars': cars, 'dealer_id': dealer_id})
    
    if request.method == 'POST':
        # Process POST request
        return process_add_review_post(request, dealer_id)

    return HttpResponseBadRequest('Invalid HTTP method')

def process_add_review_post(request, dealer_id):
    """Process POST request for add_review."""
    purchase_check = request.POST.get('purchasecheck')
    content = request.POST.get('content')
    purchasedate = request.POST.get('purchasedate')
    car_id = request.POST.get('car')

    if not (purchase_check and content and purchasedate and car_id):
        return HttpResponseBadRequest('Invalid or missing POST data')

    try:
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
        review_post_url = (
            "https://us-south.functions.appdomain.cloud/api/v1/web/"
            "54ee907b-434c-4f03-a1b3-513c235fbeb4/default/review-post"
        )

        response = requests.post(review_post_url, json=json_payload, timeout=10)
        if response.status_code == 200:
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        
        logger.error('Failed to post review. Status code: %s', response.status_code)
        return HttpResponse(f'Failed to post review. Status code: {response.status_code}', status=response.status_code)

    except Car.DoesNotExist:
        logger.error('Invalid car ID')
        return HttpResponseBadRequest('Invalid car ID')
    except ValueError:
        logger.error('Invalid date format')
        return HttpResponseBadRequest('Invalid date format')
    except Exception as e:
        logger.error('Error posting review: %s', str(e))
        return HttpResponse(f'Error posting review: {str(e)}', status=500)
  
def get_dealerships(request):
    context = {}
    dealerships = get_dealers_from_cf()  # Assuming this function fetches dealerships
    context['dealership_list'] = dealerships
    return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request):
    """Get details of a car dealer and their reviews."""
    if request.method == 'GET':
        dealer_id = request.GET.get('dealer_id')
        if not dealer_id:
            return HttpResponseBadRequest('Missing dealer_id')

        dealer_reviews = get_dealer_reviews_from_cf(dealer_id)
        for review in dealer_reviews:
            review['sentiment'] = analyze_review_sentiments(review['review'])

        context = {'dealer_reviews': dealer_reviews}
        return render(request, 'djangoapp/dealer_details.html', context)

    return HttpResponseNotAllowed('Invalid HTTP method')

def get_dealer_reviews_from_cf(dealer_id):
    """Retrieves dealer reviews from a cloud function."""
    dealer_reviews_url = (
        f"https://us-south.functions.appdomain.cloud/api/v1/web/"
        f"54ee907b-434c-4f03-a1b3-513c235fbeb4/default/myAction/{dealer_id}/reviews"
    )
    headers = {'Authorization': 'Bearer KidOOw8m-hso_lc2AgTMLdxmudJdgaJAe-dewXr62x1L'}
    response = requests.get(dealer_reviews_url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.json()
    return []

def analyze_review_sentiments(review_text):
    """Analyzes the sentiment of a review text using Watson NLU."""
    sentiment_analysis_url = (
        "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/"
        "instances/ea601f46-3769-4375-85f1-9c79b2d0f580"
    )
    headers = {'Authorization': 'Bearer KidOOw8m-hso_lc2AgTMLdxmudJdgaJAe-dewXr62x1L'}
    data = {"text": review_text}
    response = requests.post(sentiment_analysis_url, headers=headers, json=data, timeout=10)
    if response.status_code == 200:
        return response.json().get('sentiment', {}).get('document', {}).get('label', 'neutral')
    return "neutral"

# Add the new function here
def get_dealer_by_id(request, dealer_id):
    """
    Fetches details for a specific dealer by ID.
    """
    try:
        # Fetch the dealer from the database using the dealer ID
        dealer = CarDealerModel.objects.get(id=dealer_id)
        # Render a template with dealer details (you need to create this template)
        return render(request, 'djangoapp/dealer_by_id.html', {'dealer': dealer})
    except CarDealerModel.DoesNotExist:
        # If the dealer is not found, return an error message
        return HttpResponse('Dealer not found', status=404)

# ... [any other code that might be below] ...def contact(request):
    return render(request, 'djangoapp/contact.html')

