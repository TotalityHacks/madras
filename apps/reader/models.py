from django.db import models

from apps.director.models import Hackathon, Organization
from apps.registration.models import Application, Applicant

from django.contrib.auth import get_user_model


class Reader(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, related_name="reader", on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name="readers", on_delete=models.CASCADE)
    hackathons = models.ManyToManyField(Hackathon, related_name="readers")


class Rating(models.Model):
    application = models.OneToOneField(Application, related_name="rating", on_delete=models.CASCADE)


class RatingField(models.Model):
    TYPE_NUMERICAL = "numerical"
    TYPE_MULTIPLE_CHOICE = "multiple_choice"

    TYPE_CHOICES = (
        (TYPE_NUMERICAL, "Numerical"),
        (TYPE_MULTIPLE_CHOICE, "Multiple choice"),
    )

    rating = models.ForeignKey(Rating, related_name="fields", on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    prompt = models.CharField(max_length=64)
    min_number = models.IntegerField(default=-1)
    max_number = models.IntegerField(default=-1)
    options = models.TextField(default="", blank=True)


class RatingResponse(models.Model):
    reader = models.ForeignKey(Reader, related_name="ratings")
    applicant = models.ForeignKey(Applicant, related_name="ratings")
    rating_number = models.IntegerField(validators=[MinValueValidator(1)
                                       MaxValueValidator(10)])
    comments = models.TextField(default="", blank=True)
