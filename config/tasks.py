from celery import shared_task
from mail.models import Email_Compose
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=3, default_retry_delay=3)
def send_bulk_mails(self, email_compose_id):
    try:
        email_compose = Email_Compose.objects.get(pk=email_compose_id)
        send_mail(email_compose.subject, email_compose.body,
                  'ahmedsalauddin677785@gmail.com', ['antusaha990@gmail.com'], fail_silently=False)
        print("success..")
        return True
    except Exception as exc:
        print(exc)
        raise self.retry(exc=exc)
