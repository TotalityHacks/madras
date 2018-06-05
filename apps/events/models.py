from django.db import models
from ..locations.models import Location


class Category(models.Model):
    color = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def dictionary_representation(self):
        return {
            "id": self.id,
            "color": self.color,
            "name": self.name
        }


class Event(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Location)
    category = models.ForeignKey(Category)

    def __str__(self):
        return "Event: {}".format(self.title)

    def dictionary_representation(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "location": self.location.dictionary_representation(),
            "category": self.category.dictionary_representation()
        }

