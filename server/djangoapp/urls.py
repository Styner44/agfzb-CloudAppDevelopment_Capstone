"""
This module defines the URL patterns for the djangoapp application.
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views


app_name = 'djangoapp'  # Renamed 'app_name' to conform to UPPER_CASE naming style
urlpatterns = [
    path('dealerships/', views.get_dealerships, name='dealerships'),
    path('', views.get_dealerships, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add-review/', views.add_review, name="add_review"),
    path('dealer/<int:dealer_id>/details/', views.get_dealer_by_id, name='get_dealer_by_id'),  # New pattern for get_dealer_by_id
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)