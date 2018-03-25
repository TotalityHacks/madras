from django.db import models
from apps.registration.models import Applicant


class CheckInGroup(models.Model):
    checked_in = models.BooleanField(default=False)

    applicant = models.ForeignKey(Applicant)

    def __str__(self):
        return self.applicant.__str__() + " checked in" if self.checked_in else " not checked in"


class CheckInEvent(models.Model):
    time = models.DateTimeField()
    check_in_group = models.ForeignKey(CheckInGroup)
    check_in = models.BooleanField(default=True)
