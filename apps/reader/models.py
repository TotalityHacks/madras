from django.db import models

from apps.registration.models import Hackathon_Application, User
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.application.models import Application


class Rating(models.Model):
    application = models.OneToOneField(Hackathon_Application, related_name="rating", on_delete=models.CASCADE)


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
    reader = models.ForeignKey(User, related_name="given_ratings")
    application = models.ForeignKey(Application, related_name="ratings")
    rating_number = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                        MaxValueValidator(10)])
    comments = models.TextField(default="", blank=True)
