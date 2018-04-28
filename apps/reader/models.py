from django.db import models

from apps.registration.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.application.models import Application


class RatingResponse(models.Model):
    reader = models.ForeignKey(User, related_name="given_ratings")
    application = models.ForeignKey(Application, related_name="ratings")
    rating_number = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                        MaxValueValidator(10)])
    comments = models.TextField(default="", blank=True)
