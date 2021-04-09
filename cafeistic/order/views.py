from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from django.core.exceptions import ObjectDoesNotExist

from .models import OrderObject, OrderMeal
from .serializer import OrderSerializer, OrderMealSerializer

from menu.models import Meal
from account.models import Establishment

# --------------- Order -------------------------------------------------------------

# --------------- Get Cart ---------------
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_cart(request):
    if request.method == 'GET':
        data = {}
        account = request.user

        try:
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")
            order_ser = OrderSerializer(order_object)
            
            order_meals = OrderMeal.objects.filter(order_object=order_object)
            meal_ser = OrderMealSerializer(order_meals, many=True)

        
        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'current cart object not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        

        data['status'] = 'success'
        data['desc'] = 'current cart object found'
        data["data"] = {
            "order_object": order_ser.data,
            "order_meals": meal_ser.data
        }

        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Create Cart ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_cart(request):
    if request.method == 'POST':
        data = {}
        account = request.user

        try:
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")
            order_ser = OrderSerializer(order_object)

        except ObjectDoesNotExist:
            new_order = OrderObject()
            new_order.name = "Заказ"
            new_order.total_price = "0"
            new_order.status = "in_cart"
            new_order.client_user = account

            new_order.save()
            
            data['status'] = 'success'
            data['desc'] = 'new cart object created'
            return Response(data=data, status=status.HTTP_201_CREATED)

        data['status'] = 'failed'
        data['desc'] = 'current cart is not empty'

        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Add Meal To Cart ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_meal_to_cart(request):
    if request.method == 'POST':
        data = {}
        account = request.user
        request_data = request.data

        try:
            meal_id = request.data["meal_id"]
            meal_count = request.data["meal_count"]

            meal = Meal.objects.get(id=meal_id)
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")
            
            new_order_meal = OrderMeal()
            new_order_meal.meal = meal
            new_order_meal.count = meal_count
            new_order_meal.order_object = order_object

            new_order_meal.save()

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = ''
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        data['status'] = 'success'
        data['desc'] = 'current meal added to Cart'

        return Response(data=data, status=status.HTTP_200_OK)



# --------------- Clear Cart ---------------
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def clear_cart(request):
    if request.method == 'DELETE':
        data = {}
        account = request.user
        request_data = request.data

        try:
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'object not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        operation = order_object.delete()

        if operation:
            data['status'] = 'success'
            data['desc'] = 'object deleleted'
        else:
            data['status'] = 'failed'
            data['desc'] = 'object not deleleted'
    
        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Remove Cart Meal ---------------
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def rempove_cart_meal(request):
    if request.method == 'DELETE':
        data = {}
        account = request.user
        request_data = request.data

        try:
            cart_meal = OrderMeal.objects.get(id=request_data["cart_meal_id"])
        
        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'object not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        
        operation = cart_meal.delete()

        if operation:
            data['status'] = 'success'
            data['desc'] = 'object deleleted'
        else:
            data['status'] = 'failed'
            data['desc'] = 'object not deleleted'
    
        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Edit Cart Meal Count ---------------
@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def edit_cart_meal_count(request):
    if request.method == 'PUT':
        data = {}
        account = request.user
        request_data = request.data

        try: 
            cart_meal = OrderMeal.objects.get(id=request_data["cart_meal_id"])

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'object not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        cart_meal.count = request_data["count"]
        cart_meal.save()

        data['status'] = 'success'
        data['desc'] = 'current meal count edited'

        return Response(data=data, status=status.HTTP_200_OK)


# --------------- Make Order ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def make_order(request):
    if request.method == 'POST':
        data = {}
        account = request.user
        request_data = request.data

        try:
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")
            establishment = Establishment.objects.get(id=request_data["establishment_id"])

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'current cart object not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        order_object.status = "ordered"
        order_object.establishment = establishment
        order_object.save()

        data['status'] = 'success'
        data['desc'] = 'order made'

        return Response(data=data, status=status.HTTP_200_OK)