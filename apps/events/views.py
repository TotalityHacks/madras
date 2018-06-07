from apps.events.models import Event
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dateutil.parser import parse


@api_view(['GET'])
def get_events(request):
    params = request.GET
    events = Event.objects.all()
    if "category_id" in params:
        events = events.filter(category=params["category_id"])
    if "start_time" in params:
        events = events.filter(start_time__gte=parse(params["start_time"]))
    if "end_time" in params:
        events = events.filter(start_time__lte=parse(params["end_time"]))
    event_array = []
    for event in events:
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
