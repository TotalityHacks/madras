from apps.announcements.models import Announcement
from apps.checkin.views import error_response, success_data_jsonify
from rest_framework.decorators import api_view
import os
import datetime

APPROVED_NUMBERS = []  # TODO: Add numbers here


@api_view(['GET', 'POST'])
def announcements(request):
    if request.POST:
        form = request.POST
        body = form['Body']
        from_number = form['From']
        account_sid = form['AccountSid']
        if from_number in APPROVED_NUMBERS and account_sid == os.environ['TWILIO_SID']:  # TODO: Set this variable
            a = Announcement()
            a.message = body
            a.time = datetime.datetime.now()
            a.save()
        return success_data_jsonify({})
    else:
        events = Announcement.objects.all()
        event_array = []
        for event in events:
            event_array.append(event.dictionary_representation())
        return success_data_jsonify(event_array)
