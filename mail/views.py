from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
from .serializers import *
from config.tasks import send_bulk_mails, send_mails_to_specific_mail


class MailView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            subject = data.get('subject')
            body = data.get('body')
            email_addresses = data.getlist('email_addresses')
            configuration = data.get('configuration', None)
            attachments = data.getlist('attachments', None)
            print("all attachments: ", attachments)
            email_compose_serializer = EmailComposeSerializer(
                data={'subject': subject, 'body': body, 'configurations': configuration})
            if email_compose_serializer.is_valid():
                email_compose = email_compose_serializer.save()
                if attachments is not None and len(attachments) > 0:
                    for attachment in attachments:
                        Attachment.objects.create(
                            file=attachment, email_compose=email_compose)
                for email in email_addresses:
                    outbox = Outbox.objects.create(
                        email_address=email, status='pending', email_compose=email_compose)
                    send_mails_to_specific_mail.delay_on_commit(
                        outbox.email_address, email_compose.id)

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


class EmailComposeView(APIView):

    def get(self, request):
        emails = Email_Compose.objects.all()
        serializer = EmailComposeSerializerForView(emails, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ViewsSpecificMail(APIView):
    def get(self, request, id):
        outbox_entries = Outbox.objects.filter(email_compose__id=id)

        data = [
            {
                "emailId": entry.email_compose.id,
                "email_address": entry.email_address,
                "status": entry.status,
                "failed_reason": entry.failed_reason,
            }
            for entry in outbox_entries
        ]

        return Response({"data": data}, status=status.HTTP_200_OK)


class SMTPConfigurationView(APIView):
    def post(self, request):
        data = request.data
        serializer = SMTPConfigurationSerializer(data=data)
        if serializer.is_valid():
            config = serializer.save()
            return Response({
                "status": "success",
                "details": "Successfully added configuration",
                "username": config.username,
                "id": config.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "faild",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        all_configurations = SMTPConfiguration.objects.all()
        serializer = SMTPConfigurationSerializerForView(
            all_configurations, many=True)
        return Response(serializer.data)
