from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect, reverse
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {
        "title": "about us"
    }
    return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {
        "title": "contact us"
    }
    return render(request, "djangoapp/contact.html", context)

# Create a `login_request` view to handle sign in request
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

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect("djangoapp:login")
# ...

# Create a `registration_request` view to handle sign up request
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
                    email = email,
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                )
                user.set_password(pwd)
                user.save()
                message = "ok"

        context["message"] = message
        return render(request, "djangoapp/registration.html", context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    context["title"] = "Dealership Review"
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

