from django.db import models
from ..registration.models import User


class Application(models.Model):
    SAVED = 'SA'
    SUBMITTED = 'SU'
    STATUS = (
        (SAVED, 'Saved'),
        (SUBMITTED, 'Submitted')
    )
    status = models.CharField(max_length=2, choices=STATUS, default=SAVED)
    github_username = models.CharField(max_length=39, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Application: ({}) {}>".format(self.id, self.user.email)


class Question(models.Model):
    text = models.TextField()
    prefix = models.CharField(max_length=255, blank=True, default="")
    max_length = models.IntegerField(default=65535)
    type = models.CharField(max_length=255)


class Answer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
