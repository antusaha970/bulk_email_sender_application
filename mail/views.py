from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailComposeSerializer
from .models import Attachment, Outbox, Recipient
from django.db import transaction


class MailView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            print("Data from request")
            subject = data.get('subject')
            body = data.get('body')
            email_addresses = data.getlist('email_addresses')
            configuration = data.get('configuration', None)
            attachments = data.getlist('attachments', None)
            email_compose_serializer = EmailComposeSerializer(
                data={'subject': subject, 'body': body, 'configurations': configuration})
            if email_compose_serializer.is_valid():
                email_compose = email_compose_serializer.save()
                if attachments is not None and len(attachments) > 0:
                    for attachment in attachments:
                        Attachment.objects.create(
                            file=attachment, email_compose=email_compose)
                for email in email_addresses:
                    Outbox.objects.create(
                        email_address=email, status='pending', email_compose=email_compose)
                    Recipient.objects.create(
                        email_address=email, status='pending', email_compose=email_compose)
                # TODO: trigger celery worker for background mail sending
            else:
                data_with_errors = {
                    'errors': [email_compose_serializer.errors],
                    'status': 'failed',
                }
                return Response(data_with_errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'status': 'ok',
                'email_compose_id': email_compose.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            data_with_errors = {
                'errors': [{'server_error': e}],
                'status': 'failed',
            }
            return Response(data_with_errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
