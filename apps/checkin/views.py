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
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from wallet.models import Pass, Barcode, EventTicket, Location, BarcodeFormat
import os
import hashlib


@api_view(['POST'])
def get_qr_code(request):
    params = json.loads(request.body.decode("utf-8"))
    if "username" not in params:
        return error_response("You must include your username in the request.",
                              400)
    if "password" not in params:
        return error_response("You must include your password in the request",
                              400)
    user = authenticate(username=params["username"],
                        password=params["password"])
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

    token = jwt.encode({"group_id": group.id}, SECRET_KEY)

    return success_data_jsonify({
        "qr_code": group.id,
        "name": application.first_name + " " + application.last_name,
        "school": application.school,
        "token": token,
        "id": user.id
    })


@api_view(['GET'])
def wallet(request):

    headers = request.META
    if "Authorization" not in headers:
        return error_response("No authorization header provided.", 401)
    token = headers["Authorization"].split("Bearer ")[1]
    group_id = jwt.decode(token, SECRET_KEY)["group_id"]
    try:
        group = CheckInGroup.objects.get(id=group_id)
    except CheckInGroup.DoesNotExist:
        return error_response("Invalid jwt; no group exists with this id.",
                              401)

    user = group.applicant
    cardInfo = EventTicket()
    cardInfo.addPrimaryField('name', user.name, 'Name')
    cardInfo.addHeaderField('header', 'October 12-14, 2018',
                            'Brooklyn Expo Center')

    if user.school:
        cardInfo.addSecondaryField('loc', user.school, 'School')
    cardInfo.addSecondaryField('email', user.username, 'Email')

    organizationName = 'TotalityHacks'
    passTypeIdentifier = 'pass.com.totalityhacks.totalityhacks'
    teamIdentifier = "3R5J785EXT"

    passfile = Pass(cardInfo,
                    passTypeIdentifier=passTypeIdentifier,
                    organizationName=organizationName,
                    teamIdentifier=teamIdentifier)

    passfile.labelColor = 'rgb(255,255,255)'
    passfile.foregroundColor = 'rgb(255,255,255)'

    passfile.relevantDate = '2018-10-12T20:00-04:00'

    latitude = 40.728157
    longitude = -73.957797

    location = Location(latitude, longitude)
    location.distance = 600

    passfile.serialNumber = hashlib.sha256(user.username).hexdigest()
    passfile.locations = [location]
    passfile.barcode = Barcode(message=user.username, format=BarcodeFormat.QR)

    dir = os.path.dirname(__file__)

    passfile.addFile('icon.png',
                     open(os.path.join(dir, 'passbook/icon.png'), 'r'))
    passfile.addFile('icon@2x.png',
                     open(os.path.join(dir, 'passbook/icon@2x.png'), 'r'))
    passfile.addFile('icon@3x.png',
                     open(os.path.join(dir, 'passbook/icon@3x.png'), 'r'))

    passfile.addFile('logo.png',
                     open(os.path.join(dir, 'passbook/logo.png'), 'r'))
    passfile.addFile('logo@2x.png',
                     open(os.path.join(dir, 'passbook/logo@2x.png'), 'r'))
    passfile.addFile('logo@3x.png',
                     open(os.path.join(dir, 'passbook/logo@3x.png'), 'r'))

    passfile.addFile('background.png',
                     open(os.path.join(dir, 'passbook/background.png'), 'r'))
    passfile.addFile('background@2x.png',
                     open(os.path.join(dir, 'passbook/background@2x.png'),
                          'r'))
    passfile.addFile('background@3x.png',
                     open(os.path.join(dir, 'passbook/background@3x.png'),
                          'r'))

    key_path = 'secure/'  # TODO: Make sure we add the key here

    key_filename = os.path.join(dir, key_path)
    cert_filename = os.path.join(dir, 'passbook/certificate.pem')
    wwdr_filename = os.path.join(dir, 'passbook/WWDR.pem')

    password = os.environ['PASSBOOK_PASSWORD']  # TODO: Set this variable

    file = passfile.create(cert_filename, key_filename, wwdr_filename,
                           password)

    file.seek(0)

    response = HttpResponse(FileWrapper(file.getvalue()),
                            content_type='application/vnd.apple.pkpass')
    response['Content-Disposition'] = 'attachment; filename=pass.pkpass'
    return response


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
