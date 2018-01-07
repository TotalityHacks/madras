from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Hackathon(models.Model):
    name = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, related_name="hackathons", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
