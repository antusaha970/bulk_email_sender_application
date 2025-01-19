from django.test import TestCase
from faker import Faker
from django.contrib.auth.models import User
from ..models import SMTPConfiguration, Email_Compose, Recipient, Outbox


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

    def test_Recipient_model_with_valid_data(self):
        """
            Test Recipient model with valid data
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        config = SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)

        subject = self.faker.text(max_nb_chars=250)
        body = " ".join(self.faker.texts(nb_texts=5))

        email_compose = Email_Compose.objects.create(
            subject=subject, body=body, configurations=config, user=self.user)

        email_address = self.faker.email()
        status = "pending"

        recipient = Recipient.objects.create(
            email_address=email_address, status=status, email_compose=email_compose)
        self.assertEqual(email_address, recipient.email_address)
        self.assertEqual(status, recipient.status)
        self.assertEqual(email_compose.id, recipient.email_compose.id)

    def test_Outbox_model_with_valid_data(self):
        """
            Test Recipient model with valid data
        """
        username = self.faker.user_name()
        password = self.faker.password(length=8)
        config = SMTPConfiguration.objects.create(
            username=username, password=password, user=self.user)

        subject = self.faker.text(max_nb_chars=250)
        body = " ".join(self.faker.texts(nb_texts=5))

        email_compose = Email_Compose.objects.create(
            subject=subject, body=body, configurations=config, user=self.user)

        email_address = self.faker.email()
        status = "pending"

        recipient = Outbox.objects.create(
            email_address=email_address, status=status, email_compose=email_compose)
        self.assertEqual(email_address, recipient.email_address)
        self.assertEqual(status, recipient.status)
        self.assertEqual(email_compose.id, recipient.email_compose.id)
