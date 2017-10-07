from django.db import models

from django.contrib.auth.models import User
from apps.director.models import Hackathon


class Application(models.Model):
    STATUS_PREPARING = "preparing"
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_PREPARING, "Preparing"),
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    )

    name = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    hackathon = models.ForeignKey(Hackathon, related_name="applications")

    def __str__(self):
        return "{} ({})".format(self.name, self.hackathon)


class ApplicationField(models.Model):
    TYPE_MULTIPLE_CHOICE = "multiple_choice"
    TYPE_MULTIPLE_CHOICE_OTHER = "multiple_choice_other"
    TYPE_SHORT_ANSWER = "short_answer"
    TYPE_LONG_ANSWER = "long_answer"

    TYPE_CHOICES = (
        (TYPE_MULTIPLE_CHOICE, "Multiple Choice"),
        (TYPE_MULTIPLE_CHOICE_OTHER, "Multiple Choice with Other"),
        (TYPE_SHORT_ANSWER, "Short Answer"),
        (TYPE_LONG_ANSWER, "Long Answer"),
    )

    application = models.ForeignKey(Application, related_name="fields")
    ordering = models.IntegerField()
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    prompt = models.CharField(max_length=256)
    options = models.TextField(default="", blank=True)

    def __str__(self):
        return "{}. {} ({})".format(self.ordering, self.prompt, self.application)


class ApplicantTeam(models.Model):
    hackathon = models.ForeignKey(Hackathon)
    name = models.CharField(max_length=64)
    entry_code = models.CharField(max_length=64)

    def __str__(self):
        return "{} ({})".format(self.name, self.hackathon)


class Applicant(models.Model):
    user = models.OneToOneField(User, related_name="applicant")
    hackathon = models.ForeignKey(Hackathon, related_name="applicants")
    application = models.ForeignKey(Application, related_name="applicants")
    team = models.ForeignKey(ApplicantTeam, related_name="applicants", blank=True, null=True)
    data = models.TextField()

    def __str__(self):
        return "{}'s Application".format(self.user)
