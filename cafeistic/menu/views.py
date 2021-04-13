from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from django.core.exceptions import ObjectDoesNotExist

from account.models import (
    Establishment
)

from .models import (
    Category,
    Meal
)

from .serializer import (
    CategorySerializer,
    MealSerializer,
    CreateCategorySerializer,
    CreateMealSerializer
)

# --------------- CLIENT -------------------------------------------------------------

# --------------- Get Establishment Menu ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def send_qr_code(request):
    if request.method == 'POST':
        data = {}
        request_data = request.data

        if request_data["qr"] is not None:
            qr_code = request_data["qr"]

            try:
                establishment = Establishment.objects.get(qr_code=qr_code)

            except ObjectDoesNotExist:
                data['status'] = 'failed'
                data['desc'] = 'current menu not found'
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

            data['status'] = 'success'
            data['desc'] = 'current menu found'
            data["data"] = {
                "establisment_id": establishment.id
            }

        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Get Establishment Categories ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_categories(request):
    if request.method == 'POST':
        data = {}
        request_data = request.data

        if request_data["establisment_id"] is not None:
            establisment_id = request_data["establisment_id"]

            try:
                establishment = Establishment.objects.get(id=establisment_id)
                categoryies = Category.objects.filter(establishment=establishment)
                ser = CategorySerializer(categoryies, many=True)

            except ObjectDoesNotExist:
                data['status'] = 'failed'
                data['desc'] = 'categories not found'
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

            data['status'] = 'success'
            data['desc'] = 'current categories found'
            data["data"] = {
                "categories": ser.data
            }

        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Get Establishment Meals ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_meals(request):
    if request.method == "POST":
        data = {}
        request_data = request.data

        if request_data["category_id"] is not None:
            category_id = request_data["category_id"]

            try:
                category = Category.objects.get(id=category_id)
                meals = Meal.objects.filter(category=category)
                ser = MealSerializer(meals, many=True)

                if len(meals) == 0:
                    data['status'] = 'failed'
                    data['desc'] = 'meals not found'
                    return Response(data=data, status=status.HTTP_404_NOT_FOUND)

            except ObjectDoesNotExist:
                data['status'] = 'failed'
                data['desc'] = 'meals not found'
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

            data['status'] = 'success'
            data['desc'] = 'current meals found'
            data["data"] = {
                "categories": ser.data
            }

        return Response(data=data, status=status.HTTP_200_OK)



# --------------- ESTABLISHMENT -------------------------------------------------------------

# --------------- Get Establishment Categories ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_category(request):
    if request.method == "POST":
        data = {}
        account = request.user
        request_data = request.data

        ser = CreateCategorySerializer(data=request_data)
        establishment = account.establishment

        if ser.is_valid():

            category = Category()
            category.name = request_data["name"]
            category.establishment = establishment

            is_saved = category.save()

            if is_saved == False:
                data['status'] = 'failed'
                data['desc'] = 'new category not created'

            data['status'] = 'success'
            data['desc'] = 'new category created'
        
        else:
            data['status'] = 'failed'
            data['desc'] = 'request json with error'
        
    return Response(data=data, status=status.HTTP_200_OK)


# --------------- Get Establishment Categories ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_new_meal(request):
    if request.method == "POST":
        data = {}
        account = request.user
        request_data = request.data

        meal = Meal()
        ser = CreateMealSerializer(meal, data=request_data)
        
        if ser.is_valid():
            ser.save()

            data['status'] = 'success'
            data['desc'] = 'new meal created'
        
        else:
            data['status'] = 'failed'
            data['desc'] = 'request json with error'
        
    return Response(data=data, status=status.HTTP_200_OK)
