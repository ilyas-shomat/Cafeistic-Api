from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [
    path('get_cart', views.get_cart, name="get_cart"),
    path('create_cart', views.create_cart, name="create_cart"),
    path('add_meal_to_cart', views.add_meal_to_cart, name="add_meal_to_cart"),
]
