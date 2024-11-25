from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone


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

    # Champ pour la photo de profil
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # Remove username field
    username = None

    # Set email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No additional required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email or "User without email"

# Validator pour garantir l'unicité du nom de l'élection
def validate_unique_election_name(value):
    if Election.objects.filter(name=value).exists():
        raise ValidationError(f"An election with the name '{value}' already exists.")

# Validator pour garantir que les dates ne sont pas dans le passé
def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError("The date cannot be in the past.")

class Election(models.Model):
    # ID de l'élection, Django gère automatiquement un champ id unique.
    id = models.AutoField(primary_key=True)

    # Nom de l'élection, avec un validateur d'unicité
    name = models.CharField(max_length=255, validators=[validate_unique_election_name])

    # Description obligatoire
    description = models.TextField(validators=[MaxLengthValidator(1000)], null=False, blank=False)

    # Date et heure de début de l'élection, avec un validateur pour l'avenir
    start_date = models.DateTimeField(validators=[validate_future_date])

    # Date et heure de fin de l'élection, avec un validateur pour l'avenir
    end_date = models.DateTimeField(validators=[validate_future_date])

    # Liste des électeurs (nullable)
    voters = models.TextField(null=True, blank=True)

    # Liste des candidats (nullable)
    candidates = models.TextField(null=True, blank=True)

    # Vainqueur (nullable)
    winner = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name