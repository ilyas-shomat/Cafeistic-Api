from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [
    path('get_cart', views.get_cart, name="get_cart"),
    path('create_cart', views.create_cart, name="create_cart"),
    path('add_meal_to_cart', views.add_meal_to_cart, name="add_meal_to_cart"),
    path('clear_cart', views.clear_cart, name="clear_cart"),
    path('rempove_cart_meal', views.rempove_cart_meal, name="rempove_cart_meal"),
    path('edit_cart_meal_count', views.edit_cart_meal_count, name="edit_cart_meal_count"),
    path('make_order', views.make_order, name="make_order"),
    path('get_accepted_order', views.get_accepted_order, name="get_accepted_order"),
]
