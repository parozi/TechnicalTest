from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegistartionTestCase(APITestCase):
    def test_register(self):
        data = {
            "email": "o@test.com",
            "phone_number": "123456",
            "password": "123",
            "confirm_password": "123",
        }
        res = self.client.post("/api/registration/", data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_mismatch_password_register(self):
        data = {
            "email": "o@test.com",
            "phone_number": "123456",
            "password": "123",
            "confirm_password": "1232",
        }
        res = self.client.post("/api/registration/", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(res.data["non_field_errors"][0]), "Passwords mismatch")

    def test_login(self):
        User.objects.create(email="o@test.com", password="123")
        data = {
            "email": "o@test.com",
            "password": "123",
        }
        res = self.client.post("/api/login/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_false_password_login(self):
        User.objects.create(email="o@test.com", password="123")
        data = {
            "email": "o@test.com",
            "password": "1232",
        }
        res = self.client.post("/api/login/", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
