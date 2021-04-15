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
    ReadableAccountSerializer,
    ScheduleSerializer,
    WriteableScheduleSerializer
)

from .models import (
    Account, 
    Schedule
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


# --------------- Get Staff Schedule ---------------
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_staff_schedule(request):
    if request.method == "GET":
        data = {}
        account = request.user
        request_data = request.data

        try:
            staff = Account.objects.get(id=request_data["account_id"])
            schedule = Schedule.objects.get(account=staff)

            staff_ser = ReadableAccountSerializer(staff)
            schedule_ser = ScheduleSerializer(schedule)

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'staff or schedule not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        data['status'] = 'success'
        data['desc'] = 'schedule  found'
        data["data"] = {
            "staff": staff_ser.data,
            "schedule": schedule_ser.data
        }

        return Response(data=data, status=status.HTTP_200_OK)



# --------------- Edit Staff Schedule ---------------
@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def edit_staff_schedule(request):
    if request.method == "PUT":
        data = {}
        account = request.user
        request_data = request.data

        try:
            schedule = Schedule.objects.get(id=request_data["schedule_id"])
            ser = WriteableScheduleSerializer(schedule, data=request_data["schedule"], partial=True)

            if ser.is_valid():
                ser.save()

        except ObjectDoesNotExist:
            data['status'] = 'failed'
            data['desc'] = 'schedule not found'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        data['status'] = 'success'
        data['desc'] = 'schedule edited'

        return Response(data=data, status=status.HTTP_200_OK)

# --------------- Create Staff Schedule ---------------
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_staff_schedule(request):
    if request.method == "POST":
        data = {}
        account = request.user
        request_data = request.data

        try:
            check_schedule = Schedule.objects.get(account=account)
        
            data['status'] = 'failed'
            data['desc'] = 'schedule for this user already exist'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        except ObjectDoesNotExist:

            schedule = Schedule()
            schedule.account = account
            schedule.monday = False
            schedule.tuesday = False
            schedule.wednesday = False
            schedule.thursday = False
            schedule.friday = False
            schedule.saturday = False
            schedule.sunday = False

            is_save = schedule.save()

            if is_save is False:
                data['status'] = 'failed'
                data['desc'] = 'schedule not created'
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
            
            data['status'] = 'success'
            data['desc'] = 'schedule created'

        return Response(data=data, status=status.HTTP_200_OK)