"""
This module defines the URL patterns for the djangoapp application.
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from djangoapp import views

app_name = 'djangoapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', views.get_dealerships, name='djangoapp1'),
    # path('djangoapp2/', views.djangoapp, name='djangoapp2'),  # Commented out
    path('dealerships/', views.get_dealerships, name='dealerships'),
    path('', views.get_dealerships, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Ensure the following views are defined or comment them out
    # path('registration/', views.registration_request, name='registration'),
    # path('login/', views.login_request, name='login'),
    # path('logout/', views.logout_request, name='logout'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/add-review/', views.add_review, name="add_review"),
    path('dealer/<int:dealer_id>/details/', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('dealerships/', views.list_dealerships, name='dealerships'),
    path('dealership/<int:dealer_id>/', views.view_dealership, name='view_dealership'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
