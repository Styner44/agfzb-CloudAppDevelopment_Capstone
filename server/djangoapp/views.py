from django.shortcuts import render, get_object_or_404
from .restapis import get_dealer_reviews_from_cf
from django.http import JsonResponse, HttpResponseNotAllowed
import logging
from .models import CarModel, Dealer, DealerReview
import logging
import requests
import logging
from django.shortcuts import render
from .utils import get_dealer_reviews_from_cf, get_dealers_from_cf
from datetime import datetime
from .utils import post_request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car
from datetime import datetime
import requests

def add_review(request, dealer_id):
    if request.method == 'GET':
        cars = Car.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', {'cars': cars, 'dealer_id': dealer_id})

    elif request.method == 'POST':
        review = {
            'dealership': dealer_id,
            'name': request.user.username,
            'purchase': request.POST['purchasecheck'],
            'review': request.POST['content'],
            'purchase_date': datetime.strptime(request.POST['purchasedate'], '%m/%d/%Y').isoformat(),
            'car_make': Car.objects.get(id=request.POST['car']).make.name,
            'car_model': Car.objects.get(id=request.POST['car']).name,
            'car_year': Car.objects.get(id=request.POST['car']).year.year,
        }

        json_payload = {
            "review": review
        }

        # Make a POST request to the Cloudant server with json_payload
        # You need to replace 'cloudant_server' with your actual Cloudant server
        response = requests.post('cloudant_server', json=json_payload)

        if response.status_code == 200:
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        else:
            return HttpResponse('Failed to post review')

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Views for static pages
def about(request):
    # Render the about page
    context = {"title": "about us"}
    return render(request, "djangoapp/about.html", context)

def get_dealer_details(request, dealer_id):
    context = {}
    context['reviews'] = get_dealer_reviews_from_cf(dealer_id)
    return render(request, 'djangoapp/dealer_details.html', context)
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)
    return HttpResponseNotAllowed(["GET"])

# View for getting a list of all dealerships
def get_dealerships(request):
    context = {"title": "Dealership Review"}
    
    if request.method == "GET":
        try:
            # Step 2: Get the list of dealerships
            dealership_data = get_dealers_from_cf()

            # Create Dealer objects from the dealership data
            dealerships = []
            for dealer_info in dealership_data:
                new_dealer = Dealer(
                    name=dealer_info['name'],
                    city=dealer_info['city'],
                    state=dealer_info['state'],
                    st=dealer_info['st'],
                    address=dealer_info['address'],
                    full_name=dealer_info['full_name'],
                    lat=dealer_info['lat'],
                    long=dealer_info['long'],
                    short_name=dealer_info['short_name'],
                    zip=dealer_info['zip']
                )
                new_dealer.save()
                dealerships.append(new_dealer)

            # Step 3: Add the dealerships to the context
            context['dealerships'] = dealerships

            # Step 4: Render the template with the context
            return render(request, 'djangoapp/index.html', context)
        except requests.RequestException as e:
            logger.error(f"Error retrieving dealerships: {str(e)}")
            context['error'] = "Error retrieving dealerships. Please try again later."
        except ValueError as e:
            logger.error(f"Error parsing response: {str(e)}")
            context['error'] = "Error parsing response. Please try again later."

    # Render the 'index.html' template with the updated context
    return render(request, 'djangoapp/index.html', context)


# View for getting a list of all car models
def car_models():
    models = CarModel.objects.all()
    data = {"car_models": list(models.values("name", "description"))}
    return JsonResponse(data)

# View for getting reviews of a dealer
def dealer_reviews(dealer_id):
    reviews = DealerReview.objects.filter(dealer_id=dealer_id)
    data = {"dealer_reviews": list(reviews.values("name", "review", "purchase_date", "purchase", "car_make", "car_model", "car_year", "sentiment"))}
    return JsonResponse(data)

# View for updating dealer details
def update_dealer(request, dealer_id):
    if request.method == 'POST':
        # Check if the user is authenticated and is staff
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({"error": "Unauthorized"}, status=403)

        # Validate POST data
        required_fields = ['name', 'city', 'state', 'st']
        for field in required_fields:
            if field not in request.POST or not isinstance(request.POST[field], str):
                return JsonResponse({'error': f'Missing or invalid field: {field}'}, status=400)

        try:
            # Update dealer details
            dealer = Dealer.objects.get(id=dealer_id)
            dealer.name = request.POST['name']
            dealer.city = request.POST['city']
            dealer.state = request.POST['state']
            dealer.st = request.POST['st']
            dealer.save()

            return JsonResponse({'success': 'Dealer updated successfully'})
        except Dealer.DoesNotExist:
            return JsonResponse({'error': 'Dealer does not exist'}, status=404)
        except (KeyError, TypeError) as e:
            return JsonResponse({'error': f'Invalid data format: {str(e)}'}, status=400)
        except Exception as e:
            # An unexpected error occurred
            logger.error(f"Error updating dealer: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return HttpResponseNotAllowed(["POST"])

# View for posting a dealer review
def post_review(request, dealer_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        data = request.POST

        # Validate the data
        required_fields = ['content', 'rating']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)

        dealer = get_object_or_404(Dealer, id=dealer_id)

        # Create a new review
        review = DealerReview.objects.create(
            dealer=dealer,
            user=request.user,
            content=data.get("content"),
            rating=data.get("rating"),
            # Add other fields as needed
        )

        # Save the new review to the database
        review.save()

        return JsonResponse({"message": "Review posted successfully"})
    else:
        return HttpResponseNotAllowed(["POST"])
