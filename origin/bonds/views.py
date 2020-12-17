import logging
import random
import string
import requests

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    BondSerializer,
)
from .models import User, Bond
from origin.settings import TIMEOUT, LEI_LOOKUP_URL

logger = logging.getLogger(__name__)


def code_generator():
    return "".join(random.choice(string.ascii_letters) for i in range(6))


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        if request.auth is None:
            serializer = RegistrationSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                email = serializer.validated_data["email"]
                cache.set(code_generator(), email, TIMEOUT)
                message = f"{code_generator()} click on the link enter the code to activate user http://localhost/api/activate/"
                recepient = email
                subject = "activation "
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        recipient_list=[recepient],
                        from_email="",
                        fail_silently=False,
                    )
                except:
                    pass
                return Response("User Created", status=status.HTTP_201_CREATED)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                f"Request auth is not none instead {request.auth}",
                status=status.HTTP_403_FORBIDDEN,
            )


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        if request.auth is None:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = request.data["email"]
                token = Token.objects.get_or_create(user=User.objects.get(email=email))
                response = {"Logged in as": email, "token": token[0].key}
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ActivateUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data["email"]
        verification_code = request.data["verification_code"]
        if cache.get(verification_code, None) == request.data["email"]:
            user = User.objects.get(email=request.data["email"])
            user.is_active = True
            user.save()
            return Response("account activated", status=status.HTTP_200_OK)
        else:
            return Response("Enter a valid code", status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):

        return Response("loged out", status=status.HTTP_200_OK)


class RecoverMailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        code = code_generator()
        try:
            email = request.data["email"]
        except:
            return Response("Missing parameters", status=status.HTTP_400_BAD_REQUEST)
        queryset = User.objects.filter(email=email)
        get_object_or_404(queryset)
        cache.set(code, email, TIMEOUT)
        subject = "Reset your password "
        message = f"{code} click on the link to reset password bla"
        recepient = email
        send_mail(
            subject=subject,
            message=message,
            recipient_list=[recepient],
            from_email="",
            fail_silently=False,
        )
        return Response(
            f"Recovery mail sent to {email} ",
            status=status.HTTP_200_OK,
        )


class ResetPassView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            email = request.data["email"]
            verification_code = request.data["verification_code"]
            password1 = request.data["password"]
            password2 = request.data["confirm_password"]
        except:
            return Response("Missing parameters", status=status.HTTP_400_BAD_REQUEST)
        if password1 is None or password2 is None:
            raise Response(
                "password cannot be empty", status=status.HTTP_400_BAD_REQUEST
            )
        if password1 != password2:
            raise Response("Passwords mismatch", status=status.HTTP_400_BAD_REQUEST)
        queryset = User.objects.filter(email=email)
        get_object_or_404(queryset)
        if cache.get(verification_code, None) == request.data["email"]:
            user = User.objects.get(email=request.data["email"])
            user.set_password(request.data["password"])
            user.save()
            return Response("Password changed", status=status.HTTP_200_OK)


class RecoverPhoneView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            phone_number = request.data["phone_number"]
        except:
            return Response("Missing parameters", status=status.HTTP_400_BAD_REQUEST)
        queryset = User.objects.filter(phone_number=phone_number)
        get_object_or_404(queryset)
        code = code_generator()
        cache.set(code, User.objects.get(phone_number=phone_number).email, TIMEOUT)
        return Response(
            f"sms sent to  {phone_number} ",
            status=status.HTTP_200_OK,
        )


class BondsView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = BondSerializer

    def get(self, request):
        data = Bond.objects.filter(bond_owner=request.user)
        if request.query_params:
            data = Bond.objects.filter(
                bond_owner=request.user, legal_name=request.query_params["legal_name"]
            )
        serializer = BondSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BondSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            if serializer.validated_data["legal_name"] == "N/A":
                lei = serializer.validated_data["lei"]
                req = requests.request("GET", f"{LEI_LOOKUP_URL}{lei}").json()
                legal_name = [dict(i) for i in req][0]["Entity"]["LegalName"]["$"]
            serializer.save(bond_owner=request.user, legal_name=legal_name)
            return Response("Saved Bond", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")
