from django.db import models

from django.contrib.auth.models import User
from apps.admin import Hackathon, Organization


class Reader(models.Model):
	user = models.OneToOneField(User, related_name="reader")
	organization = models.ForeignKey(Organization, related_name="readers")
	hackathons = models.ManyToManyField(Hackathon, related_name="readers")


class Rating(models.Model):
	pass


class RatingField(models.Model):
	pass


class RatingResponse(models.Model):
	pass
