from .models import CheckInGroup, CheckInEvent
import qrcode
from django.utils import timezone
from .models import User
from ..application.models import Application
from ..constants.models import CONSTANTS

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
import base64
from io import BytesIO

static_path = "static/checkin/qr_codes/"


class GetQRCode(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            application = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return error_response(
                "User does not have an application.",
                (
                    "Make sure that you are logged in with the account that "
                    "created the application."
                ),
                404,
            )
        if not CONSTANTS.objects.get().DECISIONS_RELEASED:
            return error_response(
                "Decisions have not been released",
                (
                    "You can't check in until Totality has told you whether "
                    "you've been admitted."
                ),
                403,
            )
        if application.admission_status != "A":
            return error_response(
                "User has not been admitted to Totality.",
                "Current status is: {}".format(
                    application.get_admission_status_display()),
                403,
            )
        group = CheckInGroup.objects.get_or_create(applicant=request.user)[0]
        group.save()
        image = qrcode.make(group.id)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return Response({"qrcode": base64.b64encode(buffered.getvalue())})


class GetQRCodeAdmin(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        email = request.GET["email"]
        try:
            applicant = User.objects.get(email=email)
        except User.DoesNotExist:
            return error_response(
                "User does not exist.",
                "There is no user with this name in the database.",
                404,
            )
        try:
            application = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return error_response(
                "User does not have an application.",
                (
                    "Make sure that you are logged in with the account that "
                    "created the application."
                ),
                404,
            )
        if not CONSTANTS.objects.get().DECISIONS_RELEASED:
            return error_response(
                "Decisions have not been released",
                (
                    "You can't check in until Totality has told you whether "
                    "you've been admitted."
                ),
                403.
            )
        if application.admission_status != "A":
            return error_response(
                "User has not been admitted to Totality.",
                "Current status is: {}".format(
                    application.get_admission_status_display()),
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
                  "You do not have sufficient permission",
                  "Make sure your user is a member of the checkin group.",
                  403,
                )
            try:
                uuid = request.POST["id"]
            except KeyError:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    (
                        "You must include the id from the bar code in the "
                        "request body."
                    ),
                    400,
                )
            try:
                group = CheckInGroup.objects.get(id=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    "The id you specified does not exist in the database.",
                    404,
                )
            if group.checked_in:
                return error_response(
                    "User already checked in.",
                    "The user specified is already checked in.",
                    409,
                )
            group.checked_in = True
            group.save()
            event = CheckInEvent(
                check_in_group=group, check_in=True, time=timezone.now())
            event.save()
            return success_data_jsonify()
        else:
            return error_response(
              "Invalid method.", "Please use a post request.", 405)


class CheckOut(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.POST:
            if not request.user.has_perm("checkin.can_checkin"):
                return error_response(
                  "You do not have sufficient permission",
                  "Make sure your user is a member of the checkin group.",
                  403,
                )
            try:
                uuid = request.POST["id"]
            except KeyError:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    (
                        "You must include the id from the bar code in the "
                        "request body."
                    ),
                    400,
                )
            try:
                group = CheckInGroup.objects.get(id=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response(
                    "Must include id of the CheckinGroup.",
                    "The id you specified does not exist in the database.",
                    404,
                )
            if not group.checked_in:
                return error_response(
                    "User is not checked in.",
                    "A user must be checked in to be checked out.",
                    409,
                )
            event = CheckInEvent(
                check_in_group=group, check_in=False, time=timezone.now())
            group.checked_in = False
            event.save()
            group.save()
            return success_data_jsonify()
        else:
            return error_response(
                "Invalid method.", "Please use a post request.", 405)


# TODO: move the below functions to utils somewhere so everyone can use them
def success_data_jsonify(code=200):
    response = Response({})
    response.status_code = code

    return response


def error_response(title, message, code):

    error_dictionary = {'message': message, 'title': title}

    response = Response(error_dictionary)
    response.status_code = code

    return response
