from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.authtoken.models import Token
import json
from ..models import SMTPConfiguration


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
        # Set Auth token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get("/api/v1/configurations/")
        _data = response.json()
        # Assert responses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(_data), 0)

    def test_get_all_configurations_without_auth(self):
        """
            Checking Endpoint without providing the auth token
        """

        response = self.client.get("/api/v1/configurations/")
        # Assert responses
        self.assertEqual(response.status_code, 401)

    def test_setup_configuration_with_valid_data(self):
        """
            Test for setup configuration with minimum required data
        """
        aws_access_key_id = self.faker.text(max_nb_chars=20)
        aws_secret_access_key = self.faker.text(max_nb_chars=20)
        host = self.faker.text(max_nb_chars=20)
        name = self.faker.text(max_nb_chars=20)
        data = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "host": host,
            "name": name,
        }
        # Set Auth token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        _response = self.client.post(
            "/api/v1/configurations/", data=data, format="json")

        # Assert responses
        self.assertEqual(_response.status_code, 201)
        self.assertJSONEqual(json.dumps(_response.json()), json.dumps({
            "status": "success",
            "details": "Successfully added configuration"
        }))

    def test_setup_configuration_with_invalid_data(self):
        """
            Test for setup configuration with invalid 
        """
        data = {
            "username": "xxyyzz@gmail.com",
        }
        # Set Auth token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        _response = self.client.post(
            "/api/v1/configurations/", data=data, format="json")

        # Assert responses
        self.assertEqual(_response.status_code, 400)


# class SendMailAPITest(APITestCase):
#     def setUp(self):
#         self.faker = Faker()
#         self.user = User.objects.create(username=self.faker.user_name())
#         self.user.set_password(self.faker.password(length=10))
#         token, _ = Token.objects.get_or_create(user=self.user)
#         self.token = token
#         _data = {
#             "username": "ahmedsalauddin677785@gmail.com",
#             "password": "knrtmfxcgqcqqdxy",
#         }
