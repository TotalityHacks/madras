from apps.announcements.models import Announcement
from apps.checkin.views import error_response, success_data_jsonify
from rest_framework.decorators import api_view
import os
import datetime
from fcm_django.models import FCMDevice

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
            device = FCMDevice.objects.all()
            device.send_message(title=a.message)
        return success_data_jsonify({})
    else:
        all_announcements = Announcement.objects.all()
        announcement_array = []
        for announcement in all_announcements:
            announcement_array.append(announcement.dictionary_representation())
        return success_data_jsonify(announcement_array)
