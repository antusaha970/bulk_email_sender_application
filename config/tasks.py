from celery import shared_task
from mail.models import Email_Compose, Outbox, Recipient, Attachment, SMTPConfiguration
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage


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
                    for attachment in attachments:
                        email.attach_file(attachment.file.path)
                    email.send(fail_silently=False)
                    outbox.status = 'success'
                    outbox.save()
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
