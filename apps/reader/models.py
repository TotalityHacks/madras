from django.db import models

from apps.registration.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.application.models import Application


class Rating(models.Model):
    reader = models.ForeignKey(User, related_name="given_ratings")
    application = models.ForeignKey(Application, related_name="ratings")
    comments = models.TextField(default="", blank=True)

    @property
    def details(self):
        return {x.field.name: x.number for x in self.ratingresponse_set.all()}

    @property
    def rating(self):
        return sum([x.field.weight * (x.number - 1) / 4 for x in self.ratingresponse_set.all()])

    def __getattr__(self, key):
        if key.startswith("field_"):
            resp = RatingResponse.objects.filter(rating=self, field__name=key.rsplit("_", 1)[-1]).first()
            return resp.number if resp else None
        super(Rating, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key.startswith("field_") and not key.endswith("_state"):
            rating_field = RatingField.objects.get(name=key.rsplit("_", 1)[-1])
            RatingResponse.objects.create(rating=self, field=rating_field, number=value)
            return
        super(Rating, self).__setattr__(key, value)


class RatingField(models.Model):
    name = models.TextField()
    weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class RatingResponse(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    field = models.ForeignKey(RatingField, on_delete=models.CASCADE)
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
