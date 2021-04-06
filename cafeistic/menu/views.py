from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView

from account.models import (
    Establishment
)

# --------------- MENU -------------------------------------------------------------

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

            except Establishment.DoesNotExixt:
                return Response(status=status.HTTP_404_NOT_FOUND)

            data['status'] = 'success'
            data['desc'] = 'current menu found'
            data["data"] = {
                "establisment_id": establishment.id
            }

        return Response(data=data)

