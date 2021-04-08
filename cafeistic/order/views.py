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

# --------------- Order -------------------------------------------------------------

# --------------- Get Cart ---------------
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_cart(request):
    if request.method == 'GET':
        data = {}
        request_data = request.data
        account = request.user

        try:
            order_object = OrderObject.objects.get(client_user=account, status="in_cart")
            order_ser = OrderSerializer(order_object)
            
            order_meals = OrderMeal.objects.filter(order_object=order_object)
            meal_ser = OrderMealSerializer(order_meals, many=True)

        
        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'current menu not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        

        data['status'] = 'success'
        data['desc'] = 'current menu found'
        data["data"] = {
            "order_object": order_ser.data,
            "order_meals": meal_ser.data
        }

        return Response(data=data, status=status.HTTP_200_OK)
