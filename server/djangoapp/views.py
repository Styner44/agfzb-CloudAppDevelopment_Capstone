from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
import logging
from .models import CarModel, Dealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import FunctionsV1
import requests

# Assuming the following import for get_dealer_reviews_from_cf
from .utils import get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Define get_dealers_from_cf function (missing in your code)
def get_dealers_from_cf():
    # Implement the function logic here
    pass

# Views for static pages
def about(request):
    # Render the about page
    context = {"title": "about us"}
    return render(request, "djangoapp/about.html", context)

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)
    return HttpResponseNotAllowed(["GET"])

def get_dealerships(request):
    context = {"title": "Dealership Review"}
    if request.method == "GET":
        try:
            # Step 2: Get the list of dealerships
            dealership_data = get_dealers_from_cf()

            # Create Dealer objects from the dealership data
            dealerships = []
            for dealer in dealership_data:
                new_dealer = Dealer(
                    name=dealer['name'],
                    city=dealer['city'],
                    state=dealer['state'],
                    st=dealer['st'],
                    address=dealer['address'],
                    full_name=dealer['full_name'],
                    lat=dealer['lat'],
                    long=dealer['long'],
                    short_name=dealer['short_name'],
                    zip=dealer['zip']
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
def car_models(request):
    models = CarModel.objects.all()
    data = {"car_models": list(models.values("name", "description"))}
    return JsonResponse(data)

# View for getting reviews of a dealer
def dealer_reviews(request, dealer_id):
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
