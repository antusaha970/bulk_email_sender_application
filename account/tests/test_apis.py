from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status


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

        self.assertEqual(_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', _response.json())

    def test_login_with_invalid_user(self):
        """
            Test login with an user credentials that does not exist
        """
        # setup dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        # make request
        _response = self.client.post("/api/v1/account/login/", {
            'username': username,
            'password': password
        })

        # assert response
        self.assertEqual(_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_with_valid_user_invalid_credentials(self):
        """
            Test login with an user credentials that does not correct
        """
        # setup dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        User.objects.create_user(username=username, password=password)

        # make request
        _response = self.client.post("/api/v1/account/login/", {
            'username': username,
            'password': self.faker.password(length=5)
        })

        # assert response
        self.assertEqual(_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_valid_data(self):
        """
            Test registration functionally with valid data 
        """

        # prepare dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        _response = self.client.post("/api/v1/account/register/", {
            'username': username,
            'password': password
        })

        # assert response
        self.assertEqual(_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', _response.json())

    def test_registration_with_invalid_data(self):
        """
            Test registration functionally with invalid data (Like without password)
        """

        # prepare dummy data
        username = self.faker.first_name()

        _response = self.client.post("/api/v1/account/register/", {
            'username': username,
        })

        # assert response
        self.assertEqual(_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_and_login_together(self):
        """
            Test registration and login flow together and check if token exists
        """

        # prepare dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        _response = self.client.post("/api/v1/account/register/", {
            'username': username,
            'password': password
        })

        # assert registration response
        self.assertEqual(_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', _response.json())

        # check login
        _response = self.client.post("/api/v1/account/login/", {
            'username': username,
            'password': password
        })

        # assert login response
        self.assertEqual(_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', _response.json())

    def test_registration_with_duplicate_username(self):
        """
            Test registration process with duplicate username 
        """

        # dummy data
        username = self.faker.first_name()
        password = self.faker.password(length=8)

        # prepare data for test
        User.objects.create_user(username=username, password=password)

        _response = self.client.post("/api/v1/account/register/", {
            'username': username,
            'password': password
        })

        # assert response
        self.assertEqual(_response.status_code, status.HTTP_400_BAD_REQUEST)
