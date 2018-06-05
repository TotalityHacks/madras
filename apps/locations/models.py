from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=10)
    url = models.URLField()

    def dictionary_representation(self):
        return {
            "id": self.id,
            "map_title": self.title,
            "url": self.url
        }
