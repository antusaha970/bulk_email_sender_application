from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker


class AccountAPITestCase(APITestCase):
    def setUp(self):
        self.faker = Faker()

    def test_login_with_valid_user(self):
        """
            Test login with a valid user credentials and check if receiving token
        """
        # setup dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        User.objects.create_user(username=username, password=password)

        # make request
        _response = self.client.post("/api/v1/account/login/", {
            'username': username,
            'password': password
        })

        # assert response

        self.assertEqual(_response.status_code, 200)
        self.assertIn('token', _response.json())
