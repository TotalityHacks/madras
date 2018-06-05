from django.db import models
from ..locations.models import Location


class Category(models.Model):
    color = models.CharField()
    name = models.CharField()

    def dictionary_representation(self):
        return {
            "id": self.id,
            "color": self.color,
            "name": self.name
        }


class Event(models.Model):
    title = models.CharField()
    description = models.CharField()
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

