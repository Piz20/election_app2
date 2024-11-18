from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crée et retourne un utilisateur avec un email."""
        if not email:
            raise ValueError("L'email doit être fourni")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crée et retourne un superutilisateur avec un email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    matricule = models.CharField(max_length=100, null=True, blank=True, unique=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    elections = models.JSONField(null=True, blank=True)

    USERNAME_FIELD = 'email'  # Utilisez 'email' comme identifiant principal
    REQUIRED_FIELDS = []  # Aucun champ supplémentaire requis

    objects = CustomUserManager()

    def __str__(self):
        return self.email or "Utilisateur sans email"
