from django.db import models

# Create your models here.
class Application():
	github_username = models.CharField(max_length=39, blank=True, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	submission_date = models.DateTimeField(default=(datetime.now()))
