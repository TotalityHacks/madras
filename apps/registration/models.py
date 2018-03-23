from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Applicant(AbstractUser):
    github_user_name = models.CharField(max_length=39, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=200, help_text='Required', unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.email

    def get_full_name(self):
        return self.application.name


class Application(models.Model):
    STATUS_PREPARING = "preparing"
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_PREPARING, "Preparing"),
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    )
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name="application", null=True)

    name = models.CharField(max_length=128, blank=True, verbose_name='What is your name?')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    short_answer = models.CharField(max_length=500, blank=True, verbose_name='What matters to you and why?', default='')

    def __str__(self):
        return "{} ({})".format(self.name, self.hackathon)


@receiver(post_save, sender=Applicant)
def create_application(sender, instance, created, **kwargs):
    if created:
        Application.objects.create(applicant=instance)

@receiver(post_save, sender=Applicant)
def save_application(sender, instance, **kwargs):
    instance.application.save()
