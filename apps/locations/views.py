from apps.locations.models import Location
from rest_framework.decorators import api_view
from apps.checkin.views import success_data_jsonify


@api_view(['GET'])
def get_maps(request):
    locations = Location.objects.filter(show_in_maps=True)
    location_array = []
    for location in locations:
        location_array.append(location.dictionary_representation())
    return success_data_jsonify(location_array)
