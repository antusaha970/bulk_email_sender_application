from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AccountSerializer, AccountLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AccountRegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = AccountSerializer(data=data, many=False)
        if serializer.is_valid():
            account = serializer.save()
            token, _ = Token.objects.get_or_create(user=account)
            return Response({
                'token': str(token)
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountLoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = AccountLoginSerializer(data=data, many=False)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = get_object_or_404(User, username=username)
            account = authenticate(username=username, password=password)
            if account:
                token, _ = Token.objects.get_or_create(user=account)
                return Response({
                    'token': str(token),
                })
            else:
                return Response({'details': 'Invalid password or username'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
