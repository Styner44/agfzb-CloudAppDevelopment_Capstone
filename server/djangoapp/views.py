from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
from .models import CarMake, CarModel, Dealer, DealerReview
from django.shortcuts import render, redirect

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {"title": "about us"}
    return render(request, "djangoapp/about.html", context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {"title": "contact us"}
    return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign-in request
def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            context["message"] = "ok"
        else:
            context["message"] = "Invalid details"

        return render(request, "djangoapp/login.html", context)

# Create a `logout_request` view to handle sign-out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:login")

# Create a `registration_request` view to handle sign-up request
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
            message = "Passwords do not match"
        elif User.objects.filter(email=email):
            message = "Email already in use"
        else:
            try:
                User.objects.get(username=username)
                message = "User already exists. Check email and/or username"
            except User.DoesNotExist:
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

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {"title": "Dealership Review"}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create a `car_models` view to get a list of all car models
def car_models(request):
    models = CarModel.objects.all()
    data = {"car_models": list(models.values("name", "description"))}
    return JsonResponse(data)

# Create a `dealer_reviews` view to get reviews of a dealer
def dealer_reviews(request, dealer_id):
    # Assuming you have a DealerReview model with a foreign key to the Dealer model
    reviews = DealerReview.objects.filter(dealer_id=dealer_id)
    data = {"dealer_reviews": list(reviews.values())}
    return JsonResponse(data)

# Create an `update_dealer` view to update dealer details
def update_dealer(request, dealer_id):
    if request.method == "POST":
        # TODO: Add authentication check to ensure only authorized users can update
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        data = request.POST
        # TODO: Validate the data

        dealer = get_object_or_404(Dealer, id=dealer_id)

        # Example: Update dealer name and location
        dealer.name = data.get("name", dealer.name)
        dealer.location = data.get("location", dealer.location)

        # TODO: Continue updating other dealer fields as needed

        dealer.save()

        return JsonResponse({"message": "Dealer updated successfully"})
    else:
        return HttpResponseNotAllowed(["POST"])

# Create a `post_review` view to post a dealer review
def post_review(request, dealer_id):
    if request.method == "POST":
        # TODO: Add authentication check to ensure only authorized users can post reviews
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        data = request.POST
        # TODO: Validate the data

        dealer = get_object_or_404(Dealer, id=dealer_id)

        # Create a new DealerReview object with the validated data
        review = DealerReview.objects.create(
            dealer=dealer,
            title=data.get("title"),
            content=data.get("content"),
            rating=data.get("rating"),
            # TODO: Add other fields as needed
        )

        # Save the new review to the database
        review.save()

        return JsonResponse({"message": "Review posted successfully"})
    else:
        return HttpResponseNotAllowed(["POST"])
