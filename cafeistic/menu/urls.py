from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [

    ############ Categories #############
    path('send_qr', views.send_qr_code, name="login"),

]
