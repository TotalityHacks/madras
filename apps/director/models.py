from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128)


class Hackathon(models.Model):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, related_name="hackathons")
