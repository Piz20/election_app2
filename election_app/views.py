# election_app/views.py
from django.contrib.auth import authenticate, login

from .forms import CustomUserRegistrationForm, LoginForm


def index_view(request):
    return render(request, 'election_app/index.html')


from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            # Créez un utilisateur si le formulaire est valide
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash le mot de passe
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            # Messages d'erreurs ajoutés automatiquement par le formulaire
            messages.error(request, "There were errors in your form.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'election_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('about')  # Rediriger vers la page d'accueil après connexion
            else:
                # Si l'utilisateur est invalide, ajouter un message d'erreur
                messages.error(request, 'Invalid login credentials')

    else:
        form = LoginForm()

    return render(request, 'election_app/login.html', {'form': form})


def about_view(request):
    return render(request, 'election_app/about.html')


def contact_view(request):
    return render(request, 'election_app/contact.html')


def features_view(request):
    return render(request, 'election_app/features.html')
def help_view(request):
    return render(request, 'election_app/help.html')