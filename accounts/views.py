from django.shortcuts import render
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user


# Create your views here.
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created", "data": serializer.data}
            return Response(status=status.HTTP_201_CREATED, data=response)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class LoginView(APIView):

    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Successful Login", "tokens": tokens}
            return Response(status=status.HTTP_202_ACCEPTED, data=response)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Invalid Credentials"},
            )

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
