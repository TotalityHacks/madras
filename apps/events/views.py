from apps.events.models import Event
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_events(request):
    event_array = []
    for event in Event.objects.all():
        event_array.append(event.dictionary_representation())
    return success_data_jsonify(event_array)


def success_data_jsonify(data, code=200):
    response = Response({
        "success": True, "data": data, "error": None
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
