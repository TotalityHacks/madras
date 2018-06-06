from django.db import models


class Announcement(models.Model):
    message = models.CharField(max_length=200)
    time = models.DateTimeField()

    def dictionary_representation(self):
        return {
            "id": self.id,
            "message": self.message,
            "time": self.time.isoformat()
        }
