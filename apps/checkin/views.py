from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CheckInGroup, CheckInEvent
import qrcode
from django.utils import timezone
from .models import Applicant

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse

static_path = "static/checkin/qr_codes/"


class GetQRCode(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: check that applicant was actually admitted
        group = CheckInGroup(applicant=request.user)
        group.save()
        return HttpResponse(qrcode.make(group.uuid), content_type="image/png")

#
def get_qr_code(request):
    email = request.GET["email"]
    # TODO: will need to be authenticated to admins
    try:
        applicant = Applicant.objects.get(email=email)
    except Applicant.DoesNotExist:
        return error_response("User does not exist.",
                              "There is no user with this name in the database.",
                              404)
    # TODO: filter to only include admitted applicants
    try:
        group = CheckInGroup.objects.get(applicant=applicant)
    except CheckInGroup.DoesNotExist:
        group = CheckInGroup(applicant=applicant)
        group.save()
    return HttpResponse(qrcode.make(group.uuid), content_type="image/png")




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
        group.checked_in = True
        group.save()
        event = CheckInEvent(check_in_group=group, check_in=True, time=timezone.now())
        event.save()
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


