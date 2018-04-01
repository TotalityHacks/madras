from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from madras import settings
from .models import CheckInGroup, CheckInEvent
import qrcode
import os.path
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.reader.models import Applicant

static_path = "static/checkin/qr_codes/"


class GetQRCode(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: check that applicant was actually admitted
        group = CheckInGroup(applicant=request.user)
        group.save()
        return success_data_jsonify({ "qr_image_path": "/" + return_qr(group.uuid)})


def get_qr_codes(request):
    # TODO: will need to be authenticated to admins
    applicants = Applicant.objects.all()
    # TODO: filter to only include admitted applicants
    files = []
    for applicant in applicants:
        group = CheckInGroup(applicant=applicant)
        group.save()
        files.append(return_qr(group.uuid))
    return success_data_jsonify({"qr_image_paths": files})


def return_qr(uuid):
    relative_path = static_path + uuid + ".png"
    full_path = os.path.join(settings.PROJECT_ROOT, relative_path)
    if not os.path.exists(full_path):
        with open(full_path, "wb") as f:
            qrcode.make(uuid).save(f, format="PNG")
    return relative_path


@csrf_exempt
def check_in(request):
    if request.POST:
        try:
            uuid = request.POST["uuid"]
        except KeyError:
            return error_response("Must include uuid.",
                                  "You must include the user's uuid from the bar code in the request body.",
                                  400)
        try:
            group = CheckInGroup.objects.get(uuid=uuid)
        except CheckInGroup.DoesNotExist:
            return error_response("uuid does not exist",
                                  "The uuid you specified does not exist in the database.",
                                  404)
        if group.checked_in:
            return error_response("User already checked in.",
                                  "The user specified is already checked in.",
                                  409)
        event = CheckInEvent(check_in_group=group, check_in=True, time=timezone.now())
        group.checked_in = True
        event.save()
        group.save()
        return success_data_jsonify()
    else:
        return error_response("Invalid method.", "Please use a post request.", 405)
    # TODO: will need to be authenticated to admins


@csrf_exempt
def check_out(request):
    if request.POST:
        if request.POST:
            try:
                uuid = request.POST["uuid"]
            except KeyError:
                return error_response("Must include uuid.",
                                      "You must include the user's uuid from the bar code in the request body.",
                                      400)
            try:
                group = CheckInGroup.objects.get(uuid=uuid)
            except CheckInGroup.DoesNotExist:
                return error_response("uuid does not exist",
                                      "The uuid you specified does not exist in the database.",
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
def success_data_jsonify(obj={}, code=200):
    response = JsonResponse({
        'success' : True,
        'data' : obj
    })

    response.status_code = code

    return response


def error_response(title, message, code):

    error_dictionary = {'message' : message,
                        'title' : title}

    response = JsonResponse({'success' : False,
                        'error' : error_dictionary
    })
    response.status_code = code

    return response
