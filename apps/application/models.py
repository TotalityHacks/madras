import uuid

from django.db import models

from ..registration.models import User

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
    ("no_answer", "Prefer not to answer"),
)
GRAD_YEAR_CHOICES = (
    ("2019", "2019"),
    ("2020", "2020"),
    ("2021", "2021"),
    ("2022", "2022"),
    ("other", "Other"),
)
RACE_ETHNICITY_CHOICES = (
    ("am_indian_or_ak_native", "American Indian or Alaskan Native"),
    ("asian_or_pac_islander", "Asian / Pacific Islander"),
    ("black_or_af_am", "Black or African American"),
    ("hispanic", "Hispanic"),
    ("white_caucasian", "White / Caucasian"),
    ("multiple_or_other", "Multiple ethnicity / Other"),
    ("no_answer", "Prefer not to answer"),
)
STUDY_LEVEL_CHOICES = (
    ("high_school", "High School"),
    ("undergraduate", "Undergraduate"),
    ("graduate", "Graduate"),
    ("other", "Other"),
)


class Applicant(models.Model):

    ADMISSION_STATUS_ADMITTED = "admitted"
    ADMISSION_STATUS_DENIED = "denied"
    ADMISSION_STATUS_PENDING = "pending"
    ADMISSION_STATUS_WAITLISTED = "waitlisted"

    ADMISSION_STATUS_CHOICES = (
        (ADMISSION_STATUS_ADMITTED, "Admitted"),
        (ADMISSION_STATUS_DENIED, "Denied"),
        (ADMISSION_STATUS_PENDING, "Pending"),
        (ADMISSION_STATUS_WAITLISTED, "Waitlisted"),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="applicant")

    admission_status = models.CharField(
        max_length=16,
        choices=ADMISSION_STATUS_CHOICES,
        default=ADMISSION_STATUS_PENDING,
    )


class Application(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="application")

    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)

    devpost = models.CharField(max_length=64, blank=True)
    github = models.CharField(max_length=64, blank=True)
    linkedin = models.CharField(max_length=64, blank=True)
    personal_website = models.CharField(max_length=128, blank=True)
    school = models.CharField(max_length=64, blank=True)

    essay_helped = models.CharField(max_length=700, blank=True)
    essay_project = models.CharField(max_length=700, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    college_grad_year = models.CharField(
        max_length=8, choices=GRAD_YEAR_CHOICES, null=True, blank=True)

    gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES, null=True, blank=True)
    major = models.CharField(max_length=64, blank=True)
    current_study_level = models.CharField(
        max_length=16, choices=STUDY_LEVEL_CHOICES, null=True, blank=True)
    race_ethnicity = models.CharField(
        max_length=32, choices=RACE_ETHNICITY_CHOICES, null=True, blank=True)

    priority = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Application: {} ({})>".format(self.user.email, self.id)


class Submission(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    application = models.ForeignKey(
        Application, on_delete=models.PROTECT, related_name="submissions")
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="submissions")

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16)

    devpost = models.CharField(max_length=64, blank=True)
    github = models.CharField(max_length=64, blank=True)
    linkedin = models.CharField(max_length=64, blank=True)
    personal_website = models.CharField(max_length=128, blank=True)
    school = models.CharField(max_length=64)

    essay_helped = models.CharField(max_length=700, blank=True)
    essay_project = models.CharField(max_length=700, blank=True)

    age = models.PositiveIntegerField()
    college_grad_year = models.CharField(
        max_length=8, choices=GRAD_YEAR_CHOICES)

    gender = models.CharField(max_length=16, choices=GENDER_CHOICES)
    major = models.CharField(max_length=64)
    current_study_level = models.CharField(
        max_length=16, choices=STUDY_LEVEL_CHOICES)
    race_ethnicity = models.CharField(
        max_length=32, choices=RACE_ETHNICITY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)


class Resume(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="resumes")

    filename = models.CharField(max_length=512, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
