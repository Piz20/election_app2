from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a user with an email."""
        if not email:
            raise ValueError("The email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a superuser with an email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    matricule = models.CharField(max_length=100, null=True, blank=True, unique=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)  # Ensure email is required and unique
    date_of_birth = models.DateField(null=True, blank=True)
    elections = models.JSONField(null=True, blank=True)

    # Remove username field
    username = None

    # Set email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No additional required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email or "User without email"
