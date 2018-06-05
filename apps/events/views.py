from apps.events.models import Event
from rest_framework.response import Response


def get_events(request):
    return success_data_jsonify(Event.objects.all())


def success_data_jsonify(data, code=200):
    response = Response({
        "success": True, data: "data", "error": None
    })
    response.status_code = code

    return response


def error_response(message, code):


    response = Response({
        "success": False,
        "data": None,
        "error": {
            "message": message
        }
    })
    response.status_code = code

    return response
