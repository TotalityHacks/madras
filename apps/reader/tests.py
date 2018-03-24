
import mock
import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest import skip
from django.conf import settings


from .utils import get_metrics_github
from ..registration.models import Applicant
from .views import NextApplication, Rating
from ..registration.models import Application
from .models import Reader, RatingResponse
from ..director.models import Organization


class UtilsTests(TestCase):

    def setUp(self):
        self.application = Application.objects.create(
            name="Test Application",
            status=Application.STATUS_CLOSED
        )

        Application.objects.create(
            name="Test Application 2",
            status = Application.STATUS_CLOSED
            )

        self.user = Applicant.objects.create(email='test@example.com', password='testing')
        self.user2 = Applicant.objects.create(email='test2@example.com', password='testing2')
        Reader.objects.create(user=self.user, organization=Organization.objects.create(name="Test Organization"))
        self.factory = APIRequestFactory()

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)

    def test_next_applicant(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplication.as_view()(request)
        self.assertEquals(response.data["applicant_id"], self.application.id)

    def test_post_review(self):
        data = {"applicant_id": 1, "user_rating": 2, "comments": "hi"}
        request = self.factory.post('/reader/rating', json.dumps(data), content_type="application/json")
        force_authenticate(request, user=self.user)
        response = Rating.as_view()(request)
        self.assertEquals(1, RatingResponse.objects.count())

    def test_access_application_after_max_reivews(self):
        for i in range(5):
            data = {"applicant_id": self.application.id, "user_rating": 2, "comments": "hi"}
            request = self.factory.post('/reader/rating', json.dumps(data), content_type="application/json")
            force_authenticate(request, user=self.user)
            response = Rating.as_view()(request)
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplication.as_view()(request)
        print(response.data)
