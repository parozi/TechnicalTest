from django.urls import path, include
from .views import (
    RegistrationView,
    LoginView,
    RecoverMailView,
    RecoverPhoneView,
    ResetPassView,
    BondsView,
    LogoutView,
    ActivateUserView,
)

app_name = "bonds"

urlpatterns = [
    path("api/registration/", RegistrationView.as_view(), name="registration"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/password/recovery/email", RecoverMailView.as_view(), name="recover"),
    path("api/password/recovery/phone", RecoverPhoneView.as_view(), name="recover"),
    path("api/password/reset/", ResetPassView.as_view(), name="reset"),
    path("api/bonds/", BondsView.as_view(), name="bonds"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/acitave/", ActivateUserView.as_view(), name="activate"),
]
