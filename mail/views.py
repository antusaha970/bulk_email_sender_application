from django.shortcuts import render
from rest_framework import status
# from rest_framework.viewsets import 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
# Create your views here.

class EmailComposeView(APIView):
   
    def get(self):
        emails = Email_Compose.objects.all()
        serializer = EmailComposeSerializer(emails, many=True)
        return Response({"data": serializer.data},status=status.HTTP_200_OK)
    
    
    
    class ViewsSpecificMail(APIView):
        def get(self):
            outbox_entries = Outbox.objects.all()

            data = [
                {
                    "emailId": entry.email_compose.id,  
                    "email_address": entry.email_address,
                    "status": entry.status,
                    "failed_reason": entry.failed_reason,
                }
                for entry in outbox_entries
            ]

            return Response({"data": data},status=status.HTTP_200_OK)