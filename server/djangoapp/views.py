from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import logging
from .models import CarModel, Dealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import FunctionsV1

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Set up IBM Cloud Functions client
authenticator = IAMAuthenticator('AOk7Ln1k62vPK4QYt_dvblE2NKU_fFNG1wNfV6YJzcU8')
functions = FunctionsV1(authenticator=authenticator)

# Views for static pages
def about(request):
    # Render the about page
    context = {"title": "about us"}
    return render(request, "djangoapp/about.html", context)

def contact(request):
    # Render the contact page
    context = {"title": "contact us"}
    return render(request, "djangoapp/contact.html", context)

# View for handling user login
def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/login.html")

    if request.method == "POST":
        # Attempt to authenticate the user
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        user = authenticate(username=username, password=password)
        if user:
            # Log in the user if authentication is successful
            login(request, user)
            context["message"] = "ok"
        else:
            context["message"] = "Invalid details"

        return render(request, "djangoapp/login.html", context)

# View for handling user logout
def logout_request(request):
    # Log out the user and redirect to the login page
    logout(request)
    return redirect("djangoapp:login")

# View for handling user registration
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html")

    if request.method == "POST":
        context["message"] = ""

        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        pwd = request.POST.get('pwd')
        c_pwd = request.POST.get('c-pwd')

        if pwd != c_pwd:
            # Passwords do not match
            message = "Passwords do not match"
        elif User.objects.filter(email=email).exists():
            # Email is already in use
            message = "Email already in use"
        else:
            try:
                # Check if the username already exists
                User.objects.get(username=username)
                message = "User already exists. Check email and/or username"
            except User.DoesNotExist:
                # Create a new user
                user = User.objects.create(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(pwd)
                user.save()
                message = "ok"

        context["message"] = message
        return render(request, "djangoapp/registration.html", context)

# View for rendering the index page with a list of dealerships
def get_dealerships(request):
    context = {"title": "Dealership Review"}
    if request.method == "GET":
        try:
            # Call the 'dealer-get' service
            response = functions.invoke_action('Namespace-s3Y', 'dealer-get').get_result()

            # Extract the dealerships from the response
            dealerships = response.get('dealerships', [])

            # Add the dealerships to the context
            context['dealerships'] = dealerships

        except Exception as e:
            # Handle any errors that might occur during the API call
            context['error'] = f"Error retrieving dealerships: {str(e)}"

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
            dealer = Dealer.objects.get(pk=dealer_id)
            dealer.name = request.POST['name']
            dealer.city = request.POST['city']
            dealer.state = request.POST['state']
            dealer.st = request.POST['st']
            dealer.save()

            # TODO: Continue updating other dealer fields as needed

            return JsonResponse({'success': 'Dealer updated successfully'})
        except Dealer.DoesNotExist:
            return JsonResponse({'error': 'Dealer does not exist'}, status=404)
        except Exception as e:
            # An unexpected error occurred
            logger.error(f"Error updating dealer: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    else:
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
