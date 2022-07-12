from django.shortcuts import render
from rest_framework import serializers, generics
from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from accounts.serializers import LoginSerializer, AccountsSerializer
from accounts.models import User


class ListCreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountsSerializer
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email = serializer.validated_data["email"],
            password = serializer.validated_data["password"]
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"AccessToken": token.key}) 

        return Response(
            {"detail": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )    