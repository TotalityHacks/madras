from django.db import models

from django.contrib.auth.models import User
from apps.admin import Hackathon, Organization
from apps.registration import Application, Applicant


class Reader(models.Model):
    user = models.OneToOneField(User, related_name="reader")
    organization = models.ForeignKey(Organization, related_name="readers")
    hackathons = models.ManyToManyField(Hackathon, related_name="readers")


class Rating(models.Model):
    application = models.OneToOneField(Application, related_name="rating")


class RatingField(models.Model):
    TYPE_NUMERICAL = "numerical"
    TYPE_MULTIPLE_CHOICE = "multiple_choice"

    TYPE_CHOICES = (
        (TYPE_NUMERICAL, TYPE_NUMERICAL),
        (TYPE_MULTIPLE_CHOICE), (TYPE_MULTIPLE_CHOICE),
    )

    rating = modoels.ForeignKey(Rating, related_name="fields")
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    prompt = models.CharField(max_length=64)
    min_number = models.IntegerField(default=-1)
    max_number = models.IntegerField(default=-1)
    options = models.TextField(default="")


class RatingResponse(models.Model):
    reader = models.ForeignKey(Reader, related_name="ratings")
    applicant = models.ForeignKey(Applicant, related_name="ratings")
    data = models.TextField()
