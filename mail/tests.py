from django.test import TestCase
from faker import Faker
from django.contrib.auth.models import User
from .models import SMTPConfiguration, Email_Compose
from .serializers import SMTPConfigurationSerializer, EmailComposeSerializer


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

    def test_Email_Compose_model_with_valid_data(self):
        """
            Test email compose with valid data
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        config = SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)

        subject = self.faker.text(max_nb_chars=250)
        body = " ".join(self.faker.texts(nb_texts=5))

        email_compose = Email_Compose.objects.create(
            subject=subject, body=body, configurations=config, user=self.user)

        self.assertEqual(subject, email_compose.subject)
        self.assertEqual(body, email_compose.body)
        self.assertEqual(self.user.id, email_compose.user.id)


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

    def test_EmailComposeSerializer_with_valid_data(self):
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        config = SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)

        subject = self.faker.text(max_nb_chars=250)
        body = " ".join(self.faker.texts(nb_texts=5))

        _data = {
            'subject': subject,
            'body': body,
            'configurations': config.id
        }

        serializer = EmailComposeSerializer(data=_data)

        self.assertEqual(True, serializer.is_valid())
