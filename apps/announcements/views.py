from apps.announcements.models import Announcement
from apps.checkin.views import error_response, success_data_jsonify
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_announcements(request):
    events = Announcement.objects.all()
    event_array = []
    for event in events:
        event_array.append(event.dictionary_representation())
    return success_data_jsonify(event_array)
