from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), phone_number=phone_number)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        user = self.create_user(email, password=password, phone_number=phone_number)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=11, blank=False, unique=True, verbose_name="Phone Number"
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Bond(models.Model):

    isin = models.CharField(max_length=12)
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    bond_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.isin
