from django.db import models


class CONSTANTS(models.Model):
    DECISIONS_RELEASED = models.BooleanField(default=False)
