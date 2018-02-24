from django.test import TestCase
from unittest import skip

from .utils import get_metrics_github


class UtilsTests(TestCase):

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)
