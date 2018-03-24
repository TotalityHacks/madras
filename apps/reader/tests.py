import mock
import json


from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest import skip

from .utils import get_metrics_github
from ..registration.models import Applicant
from .views import NextApplication, Rating


class UtilsTests(TestCase):

    def setUp(self):
        self.user = Applicant.objects.create(email='test@example.com', password='testing')
        self.factory = APIRequestFactory()

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)

    def test_next_applicant(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplication.as_view()(request)

    def test_post_review(self):
        data = {"applicant_id": 1, "user_rating": 2, "comments": "hi"}
        request = self.factory.post('/reader/rating', json.dumps(data), content_type="application/json")
        force_authenticate(request, user=self.user)
        response = Rating.as_view()(request)
