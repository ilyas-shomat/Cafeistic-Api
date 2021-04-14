from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from django.core.exceptions import ObjectDoesNotExist


from .serializer import (
    AccountSerializer,
    EstablishmentSerializer,
    ReadableAccountSerializer
)

from .models import (
    Account
)

# --------------- USER -------------------------------------------------------------

# --------------- Registration New User ---------------
@api_view(["POST"])
def create_new_user(request):
    if request.method == 'POST':
        ser = AccountSerializer(data=request.data)
        data = {}
        if ser.is_valid():
            account = ser.save()
            data['status'] = 'success'
            data['desc'] = 'new user successfully created'
            data['data'] = {
                "full_name":account.full_name,
                "token":Token.objects.get(user=account).key
            }
        else:
            data = ser.errors
        return Response(data)



# --------------- ESTABLISHMENT -------------------------------------------------------------

# --------------- Registration New Establishment ---------------
@api_view(["POST"])
def create_new_establishment(request):
    if request.method == 'POST':
        ser = EstablishmentSerializer(data=request.data)
        data = {}
        if ser.is_valid():
            establishment = ser.save()
            data['status'] = 'success'
            data['desc'] = 'new establishment successfully created'
            data["data"] = {
                "establisment_id": establishment.id
            }
        else:
            data = ser.errors
        return Response(data)

# --------------- Get Staff List ---------------

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_staff_list(request):
    if request.method == "GET":
        data = {}
        account = request.user
        request_data = request.data

        try:
            establishment = account.establishment
            staffs = Account.objects.filter(establishment=establishment)
            
            ser = ReadableAccountSerializer(staffs, many=True)
        
        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'staffs not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        data['status'] = 'success'
        data['desc'] = 'current staffs found'
        data["data"] = {
            "staffs": ser.data
        }

        return Response(data=data, status=status.HTTP_200_OK)
