from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CustomUser, Election, Candidate


class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['name', 'matricule', 'gender', 'date_of_birth', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Vérifie que les mots de passe correspondent
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "The passwords do not match.")

        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']



class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'description', 'start_date', 'end_date', 'voters', 'winner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'voters': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'winner': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Election.objects.filter(name=name).exists():
            raise forms.ValidationError(f"An election with the name '{name}' already exists.")
        return name

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now():
            raise forms.ValidationError("The start date cannot be in the past.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data.get('start_date')

        if end_date < timezone.now():
            raise forms.ValidationError("The end date cannot be in the past.")
        if start_date and end_date <= start_date:
            raise forms.ValidationError("The end date must be later than the start date, including the time.")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            self.add_error('end_date', "The end date must be later than the start date, including the time.")
        return cleaned_data


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'bio', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Récupérer l'élection de kwargs et l'associer au formulaire
        self.election = kwargs.pop('election', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)

        if self.election:
            instance.election = self.election  # Associer l'élection
        else:
            raise ValidationError("Election is required to create a candidate.")

        if commit:
            instance.save()

        return instance

    def clean_name(self):
        name = self.cleaned_data['name']

        # Vérifier l'unicité du nom pour cette élection
        if self.election:
            if Candidate.objects.filter(name=name, election=self.election).exists():
                raise ValidationError(f"A candidate with the name '{name}' already exists for this election.")
        else:
            raise ValidationError("Election is required to create a candidate.")

        return name