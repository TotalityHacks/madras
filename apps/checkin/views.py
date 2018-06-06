from .models import CheckInGroup, CheckInEvent
import qrcode
from django.utils import timezone
from ..application.models import Application
from ..constants.models import CONSTANTS

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
from io import BytesIO
from ..events.views import error_response, success_data_jsonify
from ..registration.models import User
from django.contrib.auth import authenticate
import jwt
from madras.settings import SECRET_KEY
import json


@api_view(['POST'])
def get_qr_code(request):
    params = json.loads(request.body)
    if "username" not in params:
        return error_response("You must include your username in the request.", 400)
    if "password" not in params:
        return error_response("You must include your password in the request", 400)
    user = authenticate(username=params["username"], password=params["password"])
    if user is None:
        return error_response("Invalid Login Credentials", 401)

    try:
        application = Application.objects.get(user=user)
    except Application.DoesNotExist:
        return error_response(
            "You do not have an application.",
            404,
        )
    if not CONSTANTS.objects.get().DECISIONS_RELEASED:
        return error_response(
            "Decisions have not been released.",
            403,
        )
    if application.admission_status != "A":
        return error_response(
            "You have not been admitted to Totality.",
            403,
        )
    group = CheckInGroup.objects.get_or_create(applicant=user)[0]
    group.save()

    token = jwt.encode({"username": user.username}, SECRET_KEY)

    return success_data_jsonify({
        "qr_code": group.id,
        "name": application.first_name + " " + application.last_name,
        "school": application.school,
        "token": token,
        "id": user.id
    })


class GetQRCodeAdmin(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        email = request.GET["email"]
        try:
            applicant = User.objects.get(email=email)
        except User.DoesNotExist:
            return error_response(
                "User does not exist.",
                404,
            )
        try:
            application = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return error_response(
                "User does not have an application.",
                404,
            )
        if not CONSTANTS.objects.get().DECISIONS_RELEASED:
            return error_response(
                "Decisions have not been released",
                403.
            )
        if application.admission_status != "A":
            return error_response(
                "User has not been admitted to Totality.",
                403,
            )
        group = CheckInGroup.objects.get_or_create(applicant=applicant)[0]
        group.save()
        image = qrcode.make(group.id)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return Response({"qrcode": base64.b64encode(buffered.getvalue())})


class CheckIn(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.POST:
            if not request.user.has_perm("checkin.can_checkin"):
                return error_response(
                  "You do not have sufficient permission to check a user in.",
                  403,
                )
            try:
                uuid = request.POST["id"]
            except KeyError:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    400,
                )
            try:
                group = CheckInGroup.objects.get(id=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    404,
                )
            if group.checked_in:
                return error_response(
                    "User already checked in.",
                    409,
                )
            group.checked_in = True
            group.save()
            event = CheckInEvent(
                check_in_group=group, check_in=True, time=timezone.now())
            event.save()
            return success_data_jsonify({})
        else:
            return error_response(
              "Invalid method.", 405)


class CheckOut(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.POST:
            if not request.user.has_perm("checkin.can_checkin"):
                return error_response(
                  "You do not have sufficient permission",
                  403,
                )
            try:
                uuid = request.POST["id"]
            except KeyError:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    400,
                )
            try:
                group = CheckInGroup.objects.get(id=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    404,
                )
            if not group.checked_in:
                return error_response(
                    "User is not checked in.",
                    409,
                )
            event = CheckInEvent(
                check_in_group=group, check_in=False, time=timezone.now())
            group.checked_in = False
            event.save()
            group.save()
            return success_data_jsonify({})
        else:
            return error_response(
                "Invalid method.", 405)


