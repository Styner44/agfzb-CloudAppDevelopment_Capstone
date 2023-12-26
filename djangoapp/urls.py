"""
This module defines the URL patterns for the DjangoApp application.
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views


app_name = 'DjangoApp'  # Renamed 'app_name' to conform to UPPER_CASE naming style

urlpatterns = [
    path("kishana",views.get_dealerships,name='TEST')
    # path('', views.get_dealerships, name='index'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    # path('registration/', views.registration_request, name='registration'),
    # path('login/', views.login_request, name='login'),
    # path('logout/', views.logout_request, name='logout'),
    # path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path('dealerships/', views.dealership_list, name='dealership_list'),
    # path('dealer/<int:dealer_id>/add-review/', views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

