from django.db import models

from apps.director.models import Hackathon, Organization
from apps.registration.models import Application, Applicant

from django.contrib.auth import get_user_model

class Reader(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, related_name="reader")
    organization = models.ForeignKey(Organization, related_name="readers")
    hackathons = models.ManyToManyField(Hackathon, related_name="readers")


class Rating(models.Model):
    application = models.OneToOneField(Application, related_name="rating")


class RatingField(models.Model):
    TYPE_NUMERICAL = "numerical"
    TYPE_MULTIPLE_CHOICE = "multiple_choice"

    TYPE_CHOICES = (
        (TYPE_NUMERICAL, "Numerical"),
        (TYPE_MULTIPLE_CHOICE, "Multiple choice"),
    )

    rating = models.ForeignKey(Rating, related_name="fields")
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    prompt = models.CharField(max_length=64)
    min_number = models.IntegerField(default=-1)
    max_number = models.IntegerField(default=-1)
    options = models.TextField(default="", blank=True)


class RatingResponse(models.Model):
    reader = models.ForeignKey(Reader, related_name="ratings")
    applicant = models.ForeignKey(Applicant, related_name="ratings")
    data = models.TextField()
