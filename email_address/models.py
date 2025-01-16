from django.db import models
from django.contrib.auth.models import User


class Email_Address_List(models.Model):
    name = models.CharField(max_length=300)
    # relations
    user = models.ForeignKey(
        User, related_name="email_address_list", on_delete=models.CASCADE)

    # record keeping
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Email_Address(models.Model):
    email = models.EmailField()
    # relations
    email_address_list = models.ForeignKey(
        Email_Address_List, related_name="email_address_list", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["email", "email_address_list"]

    def __str__(self):
        return self.email
