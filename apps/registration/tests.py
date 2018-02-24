import json

from django.test import TestCase, Client

from .models import Applicant


class AuthTests(TestCase):
    def setUp(self):
        self.user = Applicant.objects.create(
            email="test@example.com",
            is_active=True
        )
        self.user.set_password("testing")
        self.user.save()
        self.client = Client()

    def test_login(self):
        data = {"username": "test@example.com", "password": "testing"}
        resp = self.client.post("/login/", json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode("utf-8"))
        self.assertTrue("token" in resp_data, resp_data)

    def test_login_fail(self):
        data = {"username": "test@example.com", "password": "wrong_password"}
        resp = self.client.post("/login/", json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration(self):
        data = {"email": "newuser@example.com", "password1": "mikeisamazing", "password2": "mikeisamazing"}
        resp = self.client.post("/registration/signup/", data=data)
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content.decode("utf-8"))

        # make sure success code is returned
        self.assertTrue(resp_data.get("success"), resp_data)

        # make sure the user exists
        self.assertTrue(Applicant.objects.filter(email="newuser@example.com").exists())
