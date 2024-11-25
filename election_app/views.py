# election_app/views.py
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserRegistrationForm, LoginForm, ProfilePictureForm, ElectionForm, CandidateForm

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Election, Candidate, CustomUser, Vote


# Décorateur pour vérifier que l'utilisateur n'est pas connecté
def user_is_not_authenticated(user):
    return not user.is_authenticated


def index_view(request):
    # Vérifiez si l'utilisateur est authentifié
    if request.user.is_authenticated:
        return redirect('elections')  # Redirige vers la vue profile
    return render(request, 'election_app/index.html')  # Sinon, affiche la page d'accueil


# Vue pour l'enregistrement, accessible uniquement si l'utilisateur n'est pas connecté
@user_passes_test(user_is_not_authenticated)
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


# Vue pour la connexion, accessible uniquement si l'utilisateur n'est pas connecté
@user_passes_test(user_is_not_authenticated)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('elections')  # Rediriger vers la page d'accueil après connexion
            else:
                # Si l'utilisateur est invalide, ajouter un message d'erreur
                messages.error(request, 'Invalid login credentials')

    else:
        form = LoginForm()

    return render(request, 'election_app/login.html', {'form': form})


# Vue pour la déconnexion
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')  # Redirige vers la page d'accueil après la déconnexion
    else:
        return redirect('index')


# Vue pour le profil, accessible uniquement aux utilisateurs connectés
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige vers la page de profil après la sauvegarde
    else:
        form = ProfilePictureForm()

    return render(request, 'election_app/profile.html', {
        'form': form,
        'user': user
    })


@login_required
def elections_view(request):
    # Récupérer toutes les élections
    elections = Election.objects.all()

    # Récupérer l'heure actuelle
    current_time = timezone.localtime(timezone.now())  # Heure locale (avec fuseau horaire du Cameroun, si configuré)

    # Séparer les élections en "Upcoming" et "Past"
    upcoming_elections = elections.filter(end_date__gt=current_time).order_by('start_date')
    past_elections = elections.filter(end_date__lt=current_time).order_by('-end_date')

    return render(request, 'election_app/elections.html', {
        'upcoming_elections': upcoming_elections,
        'past_elections': past_elections,
        'current_time': current_time,
    })


@login_required
def create_election_view(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            # Si le formulaire est valide, on sauvegarde l'élection
            form.save()
            response_data = {
                'success': True,
                'message': 'Election created successfully!',
            }
            return JsonResponse(response_data)
        else:
            # Si le formulaire contient des erreurs, récupérer et structurer les erreurs
            error_messages = {}
            for field, errors in form.errors.items():
                error_messages[field] = [error for error in errors]  # Liste des erreurs par champ

            print(error_messages)  # Debug : Affiche les erreurs dans la console pour le développement

            # Retourner un JsonResponse avec les erreurs structurées
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': error_messages
            })

    else:
        # Pour une requête GET ou une autre méthode, créer un formulaire vierge
        form = ElectionForm()

    return render(request, 'election_app/elections.html', {'form': form})


@login_required
def election_details_view(request, election_id):
    # Récupérer l'élection ou retourner une erreur 404 si non trouvée
    election = get_object_or_404(Election, id=election_id)

    # Récupérer les candidats liés à l'élection
    candidates = Candidate.objects.filter(election=election)

    # Obtenir la date et l'heure actuelles
    current_time = timezone.localtime(timezone.now())  # Heure locale (avec fuseau horaire du Cameroun, si configuré)

    # Transmettre les données à la vue
    context = {
        'election': election,
        'candidates': candidates,
        'now': current_time,  # Ajouter l'heure actuelle au contexte
    }
    return render(request, 'election_app/election_details.html', context)


@login_required
def add_candidate_view(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, election=election)  # Passer l'élection au formulaire
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election  # Associer l'élection
            candidate.save()  # Sauvegarder le candidat
            return JsonResponse({"success": True, "message": "Candidate added successfully!"})
        else:
            # Affichage des erreurs dans la console
            print(f"Errors: {form.errors}")
            return JsonResponse(
                {"success": False, "errors": form.errors, "message": "Please correct the errors in the form."})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})



def about_view(request):
    return render(request, 'election_app/about.html')


def contact_view(request):
    return render(request, 'election_app/contact.html')


def features_view(request):
    return render(request, 'election_app/features.html')


def help_view(request):
    return render(request, 'election_app/help.html')
