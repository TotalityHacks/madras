from .models import CheckInGroup, CheckInEvent
import qrcode
from django.utils import timezone
from .models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

static_path = "static/checkin/qr_codes/"


class GetQRCode(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: check that applicant was actually admitted
        group = CheckInGroup.objects.get_or_create(applicant=request.user)
        group.save()
        return HttpResponse(qrcode.make(group.id), content_type="image/png")


class GetQRCodeAdmin(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        email = request.GET["email"]
        try:
            applicant = User.objects.get(email=email)
        except User.DoesNotExist:
            return error_response("User does not exist.",
                                  "There is no user with this name in the database.",
                                  404)
        # TODO: filter to only include admitted applicants
        group = CheckInGroup.objects.get_or_create(applicant=applicant)
        group.save()
        return HttpResponse(qrcode.make(group.id), content_type="image/png")


class CheckIn(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        if request.POST:
            try:
                uuid = request.POST["id"]
            except KeyError:
                return error_response("Must include id of the CheckinGroup.",
                                      "You must include the id from the bar code in the request body.",
                                      400)
            try:
                group = CheckInGroup.objects.get(id=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response("Must include id of the CheckinGroup.",
                                      "The id you specified does not exist in the database.",
                                      404)
            if group.checked_in:
                return error_response("User already checked in.",
                                      "The user specified is already checked in.",
                                      409)
            group.checked_in = True
            group.save()
            event = CheckInEvent(check_in_group=group, check_in=True, time=timezone.now())
            event.save()
            return success_data_jsonify()
        else:
            return error_response("Invalid method.", "Please use a post request.", 405)
        # TODO: will need to be authenticated to admins


class CheckOut(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        if request.POST:
            if request.POST:
                try:
                    uuid = request.POST["id"]
                except KeyError:
                    return error_response("Must include the CheckInGroup's id.",
                                          "You must include the user's id from the bar code in the request body.",
                                          400)
                try:
                    group = CheckInGroup.objects.get(id=uuid)
                except CheckInGroup.DoesNotExist:
                    return error_response("Must include the CheckInGroup's id.",
                                          "The id you specified does not exist in the database.",
                                          404)
                if not group.checked_in:
                    return error_response("User is not checked in.",
                                          "A user must be checked in to be checked out.",
                                          409)
                event = CheckInEvent(check_in_group=group, check_in=False, time=timezone.now())
                group.checked_in = False
                event.save()
                group.save()
                return success_data_jsonify()
            else:
                return error_response("Invalid method.", "Please use a post request.", 405)
            # TODO: will need to be authenticated to admins


# TODO: move the below functions to utils somewhere so everyone can use them
def success_data_jsonify(code=200):
    response = Response({
    })
    response.status_code = code

    return response


def error_response(title, message, code):

    error_dictionary = {'message': message,
                        'title': title}

    response = Response(error_dictionary)
    response.status_code = code

    return response
