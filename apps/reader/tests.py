import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest import skip

from .utils import get_metrics_github
from ..registration.models import User
from .views import NextApplicationView, RatingView
from ..application.models import Application, Submission
from .models import Rating


class UtilsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com', password='testing', is_staff=True)
        self.user2 = User.objects.create(
            email='test2@example.com', password='testing2')

        self.application = Application.objects.create(
            user=self.user)
        self.application2 = Application.objects.create(
            user=self.user2)

        self.submission = Submission.objects.create(
            application=self.application,
            user=self.user,
            age=21,
        )
        self.submission2 = Submission.objects.create(
            application=self.application2,
            user=self.user2,
            age=21,
        )

        self.factory = APIRequestFactory()

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)

    def test_next_applicant(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplicationView.as_view()(request)
        self.assertEquals(response.data["id"], str(self.submission.id))

    def test_next_applicant_after_review(self):
        # Create review
        data = {
            "application": str(self.application.id),
            "field_skill": 2,
            "field_community": 5,
            "field_passion": 3,
            "comments": "hi",
        }
        request = self.factory.post(
            '/reader/rating',
            json.dumps(data),
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)
        RatingView.as_view()(request)
        self.assertEquals(1, Rating.objects.count())

        # Ensure that the 2nd application is shown
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplicationView.as_view()(request)
        self.assertEquals(response.data["id"], str(self.submission2.id))

    def test_post_review(self):
        data = {
            "application": str(self.application.id),
            "field_skill": 2,
            "field_community": 5,
            "field_passion": 3,
            "comments": "hi",
        }
        request = self.factory.post(
            '/reader/rating',
            json.dumps(data),
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)
        RatingView.as_view()(request)
        self.assertEquals(1, Rating.objects.count())

    def test_permission_denied(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user2)
        response = NextApplicationView.as_view()(request)
        self.assertEquals(403, response.status_code)
