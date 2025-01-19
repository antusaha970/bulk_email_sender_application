from django.test import TestCase
from faker import Faker
from django.contrib.auth.models import User
from .models import SMTPConfiguration
from .serializers import SMTPConfigurationSerializer


class ModelTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User(username=self.faker.first_name)
        self.user.set_password(self.faker.password(length=10))
        self.user.save()

    def test_SMTPConfiguration_model_with_valid_data(self):
        """
            Test case for SMTP configuration Model with valid data
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        config = SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)

        self.assertEqual(config.username, username)
        self.assertEqual(config.password, password)
        self.assertEqual(config.user.id, self.user.id)


class SerializerTest(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.user = User(username=self.faker.first_name)
        self.user.set_password(self.faker.password(length=10))
        self.user.save()

    def test_SMTPConfigurationSerializer_with_valid_data(self):
        """
            Test for the SMTP configuration serializer with valid data
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        data = {
            'username': username,
            'password': password
        }
        serializer = SMTPConfigurationSerializer(
            data=data, context={'user': self.user})

        self.assertEqual(True, serializer.is_valid())

    def test_SMTPConfigurationSerializer_with_duplicate_username(self):
        """
            Test for the SMTP configuration serializer with invalid data like(Duplicate Username)
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)
        data = {
            'username': username,
            'password': password
        }
        serializer = SMTPConfigurationSerializer(
            data=data, context={'user': self.user})

        self.assertEqual(False, serializer.is_valid())
