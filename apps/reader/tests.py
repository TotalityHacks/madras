from django.test import TestCase

from .utils import get_metrics_github


class UtilsTests(TestCase):
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)
