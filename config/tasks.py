from celery import shared_task
from mail.models import Email_Compose, Outbox, Recipient, Attachment, SMTPConfiguration
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from smtplib import SMTPException
from django.core.validators import validate_email
from django.db import transaction

from twilio.rest import Client
from bulk_sms.models import SmsRecipients, SandBox, SmsConfiguration, SmsCompose


@shared_task(bind=True, max_retries=3, default_retry_delay=3)
def send_bulk_mails(self, email_compose_id):
    try:
        try:
            email_compose = Email_Compose.objects.get(pk=email_compose_id)
            attachments = Attachment.objects.filter(
                email_compose=email_compose)
            config = SMTPConfiguration.objects.get(
                pk=email_compose.configurations.id)

            email_backend = EmailBackend(
                host='smtp.gmail.com',
                port=587,
                username=config.username,
                password=config.password,
                use_tls=True,
                fail_silently=False,
            )
            outboxs = Outbox.objects.filter(email_compose=email_compose)
            for outbox in outboxs:
                try:
                    # Create the email message
                    email = EmailMessage(
                        subject=email_compose.subject,
                        body=email_compose.body,
                        from_email='antu.digi.88@gmail.com',
                        to=[outbox.email_address],
                        connection=email_backend,  # Pass the custom backend

                    )
                    email.extra_headers = {
                        'Return-Path': 'antu.digi.88@gmail.com'}
                    for attachment in attachments:
                        email.attach_file(attachment.file.path)
                    try:
                        email.send(fail_silently=False)
                        outbox.status = 'success'
                        outbox.save()
                    except SMTPException as e:
                        print("Error while sending mail: ", e)

                    Recipient.objects.create(
                        email_address=outbox.email_address, email_compose=outbox.email_compose, status="success")
                except Exception as e:
                    print(e)
            print("success..")
            return True
        except Exception as e:
            print("Error ....")
            print(e)
    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=3)
def send_mails_to_specific_mail(self, email, email_compose_id):
    print("Task received for mail: ", email)
    try:
        validate_email(email)
        try:
            email_compose = Email_Compose.objects.get(pk=email_compose_id)
            attachments = Attachment.objects.filter(
                email_compose=email_compose)
            config = SMTPConfiguration.objects.get(
                pk=email_compose.configurations.id)

            email_backend = EmailBackend(
                host='smtp.gmail.com',
                port=587,
                username=config.username,
                password=config.password,
                use_tls=True,
                fail_silently=False,
            )
            outbox = Outbox.objects.get(
                email_compose=email_compose, email_address=email)

            try:
                with transaction.atomic():
                    # Create the email message
                    email = EmailMessage(
                        subject=email_compose.subject,
                        body=email_compose.body,
                        from_email='antu.digi.88@gmail.com',
                        to=[outbox.email_address],
                        connection=email_backend,  # Pass the custom backend
                    )
                    email.extra_headers = {
                        'Return-Path': 'antu.digi.88@gmail.com'}
                    for attachment in attachments:
                        email.attach_file(attachment.file.path)
                    try:
                        email.send(fail_silently=False)
                        outbox.status = 'success'
                        outbox.save()
                        Recipient.objects.create(
                            email_address=outbox.email_address, email_compose=outbox.email_compose, status="success")
                    except SMTPException as e:
                        outbox.status = 'failed'
                        outbox.save()
                        self.retry(exc=exc)

            except Exception as e:
                print(e)
            print("success..")
            return True
        except Exception as e:
            print("Error ....")
            print(e)
            raise self.retry(exc=exc)
    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)



# bind=True, max_retries=3, default_retry_delay=3

@shared_task
def send_sms_task(body, sender_number, recipient_number, sms_compose_id, config_id):
    try:
        sms_config = SmsConfiguration.objects.get(id=config_id)
        client = Client(sms_config.account_sid, sms_config.auth_token)

        # Send SMS using Twilio
        message = client.messages.create(
            body=body,
            from_=sender_number,
            to=recipient_number,
           
        )

        # Log success
        SmsRecipients.objects.create(
            phone_number=recipient_number,
            sms_compose_id=sms_compose_id,
            status='success',
            failed_reason="None"
        )
        SandBox.objects.create(
            sms_compose_id=sms_compose_id,
            sender_number=sender_number,
            recipient_number=recipient_number
        )
        return  {"recipient_number": recipient_number, "status": "success", "sid": message.sid}

    except Exception as e:
        # Log failure
        SmsRecipients.objects.create(
            phone_number=recipient_number,
            sms_compose_id=sms_compose_id,
            status='failed',
            failed_reason=str(e)
        )
        return {"recipient_number": recipient_number, "status": "failed", "reason": str(e)}

