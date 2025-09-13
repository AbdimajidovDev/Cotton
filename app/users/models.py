from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import FileExtensionValidator

from django.db import models
import uuid

from rest_framework_simplejwt.tokens import RefreshToken

from app.users.validations import validate_phone_number, check_image_size
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Login is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class UserRoles(models.TextChoices):
        ADMIN = 'a', "admin"
        REGION = 'r', 'region'
        DISTRICT = 'd', 'district'
        MASSIVE = 'm', 'massive'
        NEIGHBORHOOD = 'n', 'neighborhood'
        SQUAD = 'sd', 'squad'
        SCALESMAN = 'sm', 'scalesman'
        SHTAB = 'sh', 'shtab'
        DRIVER = 'dr', 'driver'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=40, unique=True, validators=[validate_phone_number, ])
    image = models.ImageField(upload_to='images/users/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp', 'heic', 'heif', 'avif']),
        check_image_size
    ], null=True, blank=True)
    role = models.CharField(max_length=10, choices=UserRoles.choices)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'role']
    objects = UserManager()

    def __str__(self):
        return self.full_name

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        db_table = 'user'


class SquadExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/users/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"


class NeighborhoodExcelUpload(models.Model):
    file = models.FileField(upload_to="uploads/users/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Excel: {self.file.name}"