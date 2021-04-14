from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [

    ############ COMMON #############
    # path('login/', views.login, name="login_user"),
    path('login', obtain_auth_token, name="login"),
    path('create_user', views.create_new_user, name="create_new_user"),

    ############ ESTABLISHMENT #############
    path('create_establisment', views.create_new_establishment, name="create_new_establishment"),
    path('get_staff_list', views.get_staff_list, name="get_staff_list"),
    path('get_staff_schedule', views.get_staff_schedule, name="get_staff_schedule"),
    path('edit_staff_schedule', views.edit_staff_schedule, name="edit_staff_schedule"),
    path('create_staff_schedule', views.create_staff_schedule, name="create_staff_schedule"),

]
