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
    email = models.EmailField(unique=True, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    elections = models.JSONField(null=True, blank=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Remove username field
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or "User without email"


def validate_future_date(value):
    """Validation to ensure date is not in the past."""
    if value < timezone.now():
        raise ValidationError("The date cannot be in the past.")


class Election(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, validators=[MaxLengthValidator(255)])
    description = models.TextField(validators=[MaxLengthValidator(1000)], null=False, blank=False)
    start_date = models.DateTimeField(validators=[validate_future_date])
    end_date = models.DateTimeField(validators=[validate_future_date])
    voters = models.ManyToManyField(CustomUser, related_name='voted_elections', blank=True)
    winner = models.ForeignKey(
        'Candidate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='elections_won'
    )

    def clean(self):
        """Ensure start_date is before end_date."""
        if self.start_date >= self.end_date:
            raise ValidationError("The start date must be before the end date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F("end_date")),
                name="check_start_date_before_end_date"
            ),
        ]


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates'  # Reverse relationship accessible via `election.candidates`
    )
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=1000, null=False, blank=False)
    vote_count = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.election.name}"


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def clean(self):
        """Ensure a user can only vote once per election, but can change their vote."""
        # Vérifiez si l'utilisateur a déjà voté dans cette élection
        existing_vote = Vote.objects.filter(user=self.user, candidate__election=self.candidate.election)

        # Si l'utilisateur a déjà voté pour un autre candidat, on lui permet de changer de vote
        if existing_vote.exists():
            if existing_vote.first().candidate != self.candidate:
                pass  # L'utilisateur change son vote, donc aucune validation n'est nécessaire
            else:
                pass  # L'utilisateur a déjà voté pour le même candidat, rien à faire

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} -> {self.candidate.name}"