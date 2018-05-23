import uuid

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
    type = models.CharField(max_length=255, help_text='Indicates what kind of input this question accepts (ex: short response, text field, etc).')
    required = models.BooleanField(default=False, help_text='Indicates whether users are required to fill out this question'
                                                            ' before submitting the application.')

    def __str__(self):
        return "<Question: {}>".format(self.text[:140])

    @property
    def choices(self):
        if not self.type == 'choice':
            return None
        return Choice.objects.filter(question=self).order_by('value').values_list('value', flat=True)


class Answer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('application', 'question')

    def __str__(self):
        return "<Answer: ({}) {}>".format(self.application.id, self.question.text[:140])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()


class Resume(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="resumes")

    filename = models.CharField(max_length=512, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
