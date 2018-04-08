import json

from django.test import TestCase, Client
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import User
from .tokens import account_activation_token


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
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

    def test_login_fail_not_active(self):
        u = self.user
        u.is_active = False
        u.save()

        data = {"username": "test@example.com", "password": "testing"}
        resp = self.client.post("/login/", json.dumps(data), content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration(self):
        data = {"email": "newuser@example.com", "password": "mikeisamazing"}
        resp = self.client.post("/registration/signup/", data=data)
        self.assertEqual(resp.status_code, 201)
        resp_data = json.loads(resp.content.decode("utf-8"))

        # make sure success code is returned
        self.assertTrue(resp_data.get("success"), resp_data)

        # make sure the user exists
        new_user = User.objects.filter(email="newuser@example.com")
        self.assertTrue(new_user.exists())
        new_user = new_user.first()

        # make sure token activation works
        uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode("utf-8")
        token = account_activation_token.make_token(new_user)
        resp = self.client.get("/registration/activate/{}/{}/".format(uid, token))
        self.assertEqual(resp.status_code, 200)

        # make sure account is activated
        self.assertTrue(User.objects.get(email="newuser@example.com").is_active)

    def test_registration_staff(self):
        data = {"email": "test@totalityhacks.com", "password": "wowastaffuser"}
        resp = self.client.post("/registration/signup/", data=data)
        self.assertEqual(resp.status_code, 201)

        user = User.objects.filter(email="test@totalityhacks.com")
        self.assertTrue(user.exists())
        self.assertTrue(user[0].is_staff)
