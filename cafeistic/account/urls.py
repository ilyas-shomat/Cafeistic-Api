from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [

    ############ COMMON #############
    # path('login/', views.login, name="login_user"),
    path('login', obtain_auth_token, name="login"),
    path('create_user', views.create_new_user, name="create_new_user"),
    path('create_establisment', views.create_new_establishment, name="create_new_establishment"),

]
