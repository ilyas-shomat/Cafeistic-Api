from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [

    # --------------- CLIENT -------------------------------------------------------------
    path('send_qr', views.send_qr_code, name="send_qr_code"),
    path('get_categories', views.get_categories, name="get_categories"),
    path('get_meals', views.get_meals, name="get_meals"),

    # --------------- ESTABLISHMENT -------------------------------------------------------------
    path('add_category', views.add_category, name="add_category"),

]
