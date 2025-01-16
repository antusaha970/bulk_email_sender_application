from django.db import models
from django.contrib.auth.models import User



class SmsConfiguration(models.Model):
    username = models.CharField(max_length=100)
    account_sid = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=100)
    sender_number = models.CharField(max_length=20)
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="sms_configaration",null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.sender_number})"

class SmsCompose(models.Model):
    body = models.TextField()
    sms_configuration = models.ForeignKey(SmsConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    recipient_number = models.CharField(max_length=200)
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="sms_compose",null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.recipient_number

STATUS_CHOICES = [
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('pending', 'Pending'),
]

class SmsRecipients(models.Model):
    phone_number = models.CharField(max_length=100)
    sms_compose = models.ForeignKey(SmsCompose, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    failed_reason = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.phone_number} - Status: {self.status}"



class SandBox(models.Model):
    sms_compose = models.ForeignKey(SmsCompose, on_delete=models.CASCADE)
    sender_number = models.CharField(max_length=100)
    recipient_number = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sender: {self.sender_number} to Recipient: {self.recipient_number}"
    



# class Email_Address_List(models.Model):
#     name = models.CharField(max_length=300)
#     # relations
#     user = models.ForeignKey(
#         User, related_name="email_address_list", on_delete=models.CASCADE)

#     # record keeping
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class RecipientNumberExcel(models.Model):
#     phone_number = models.()
#     # relations
#     email_address_list = models.ForeignKey(
#         Email_Address_List, related_name="sms_reci", on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ["email", "email_address_list"]

#     def __str__(self):
#         return self.email