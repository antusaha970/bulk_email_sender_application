from django.test import TestCase
from faker import Faker
from django.contrib.auth.models import User
from ..models import SMTPConfiguration
from ..serializers import SMTPConfigurationSerializer, EmailComposeSerializer


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
        aws_access_key_id = self.faker.text(max_nb_chars=20)
        aws_secret_access_key = self.faker.text(max_nb_chars=20)
        host = self.faker.text(max_nb_chars=20)
        name = self.faker.text(max_nb_chars=20)

        data = {
            'aws_access_key_id': aws_access_key_id,
            'aws_secret_access_key': aws_secret_access_key,
            'host': host,
            'name': name,
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

    def test_EmailComposeSerializer_with_invalid_data(self):

        subject = self.faker.text(max_nb_chars=250)
        body = " ".join(self.faker.texts(nb_texts=5))

        _data = {
            'subject': subject,
            'body': body,
            'configurations': 10
        }

        serializer = EmailComposeSerializer(data=_data)

        self.assertEqual(False, serializer.is_valid())
