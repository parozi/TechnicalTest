import logging

from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from .models import User, Bond
from .currencies import CURRENCIES
from origin.settings import DATE_INPUT_FORMATS

logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.IntegerField()

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data.get("email")
        password1 = data.get("password")
        password2 = data.get("confirm_password")

        user = User.objects.filter(email=email)

        if user.exists():
            raise serializers.ValidationError("User already exists")

        if password1 is None or password2 is None:
            raise serializers.ValidationError("Empty password")

        if password1 != password2:
            raise serializers.ValidationError("Passwords mismatch")

        data.pop("confirm_password", None)

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        try:
            user = User.objects.get(email=email, password=password)
        except:
            raise serializers.ValidationError(
                "A user with this email and password is not found."
            )
        update_last_login(None, User.objects.get(email=email, password=password))
        return data


class BondSerializer(serializers.ModelSerializer):

    isin = serializers.CharField(max_length=12)
    currency = serializers.CharField(max_length=3)
    maturity = serializers.DateField(input_formats=DATE_INPUT_FORMATS)
    lei = serializers.CharField(max_length=20)
    size = serializers.IntegerField(default=0)
    legal_name = serializers.CharField(required=False)

    class Meta:
        model = Bond
        fields = ["isin", "currency", "maturity", "lei", "size", "legal_name"]

    def validate(self, data):
        isin = data.get("isin", None)
        size = data.get("size", None)
        currency = data.get("currency", None)
        maturity = data.get("maturity", None)
        lei = data.get("lei", None)
        legal_name = data.get("legal_name", None)
        if isin is None:
            raise serializers.ValidationError("Please enter a valid isin.")
        if size is None:
            raise serializers.ValidationError("Please enter a valid size.")
        if currency is None or currency not in [i[0] for i in CURRENCIES]:
            raise serializers.ValidationError("Please enter a valid currency.")
        if lei is None:
            raise serializers.ValidationError("Please enter a valid lei.")
        if maturity is None:
            raise serializers.ValidationError("Please enter a valid maturity.")
        if legal_name is None:
            data["legal_name"] = "N/A"

        return data
