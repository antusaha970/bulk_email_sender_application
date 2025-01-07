from django.db import models


class SMTPConfiguration(models.Model):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=[
        ('gmail', 'Gmail'),
        ('personal', 'Personal Domain'),
        ('ses', 'Amazon SES'),
    ], default="gmail")
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)

    password = models.CharField(max_length=255, null=True, blank=True)
    use_tls = models.BooleanField(default=True, null=True, blank=True)
    use_ssl = models.BooleanField(default=False, null=True, blank=True)
    aws_access_key_id = models.CharField(max_length=255, null=True, blank=True)
    aws_secret_access_key = models.CharField(
        max_length=255, null=True, blank=True)
    aws_region = models.CharField(max_length=50, null=True, blank=True)
    ses_configuration_set = models.CharField(
        max_length=255, null=True, blank=True)
    iam_role_arn = models.CharField(max_length=255, null=True, blank=True)
    enable_tracking = models.BooleanField(default=False)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Email_Compose(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    configurations = models.OneToOneField(
        SMTPConfiguration, on_delete=models.SET_NULL, null=True, blank=True)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    file = models.FileField(upload_to="attachmentsFiles/")
    email_compose = models.ForeignKey(Email_Compose, on_delete=models.CASCADE)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_compose.subject


STATUS_CHOICES = [
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('pending', 'Pending'),
]


class Recipient(models.Model):
    email_address = models.EmailField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    email_compose = models.ForeignKey(Email_Compose, on_delete=models.CASCADE)
    failed_reason = models.CharField(
        max_length=255, blank=True, null=True, default=None)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_address


class Outbox(models.Model):
    email_address = models.EmailField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    email_compose = models.ForeignKey(Email_Compose, on_delete=models.CASCADE)
    failed_reason = models.CharField(
        max_length=255, blank=True, null=True, default=None)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_address
