from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for about page
    path('about/', views.about, name="about"),

    # path for contact page
    path('contact/', views.contact, name="contact"),

    # path for registration
    path('register/', views.registration_request, name="register"),

    # path for login
    path('login/', views.login_request, name="login"),

    # path for logout
    path('logout/', views.logout_request, name="logout"),

    # path for dealer reviews view
    path('dealer_reviews/<int:dealer_id>/', views.dealer_reviews, name="dealer_reviews"),

    # path for add a review view
    path('post_review/<int:dealer_id>/', views.post_review, name="post_review"),

    # path for dealer details view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # default path for index (homepage)
    path('', views.get_dealerships, name='index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
