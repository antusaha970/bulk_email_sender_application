from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.authtoken.models import Token


class MailAPITest(APITestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.create(username=self.faker.user_name())
        self.user.set_password(self.faker.password(length=10))
        token, _ = Token.objects.get_or_create(user=self.user)
        self.token = token

    def test_get_all_configurations_with_auth(self):
        """
            Get all configurations with auth provided
        """

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/api/v1/configurations/")
        _data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(_data), 0)

    def test_get_all_configurations_without_auth(self):
        """
            Checking Endpoint without providing the auth token
        """

        response = self.client.get("/api/v1/configurations/")

        self.assertEqual(response.status_code, 401)
