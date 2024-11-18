# election_app/views.py

from django.shortcuts import render


def index_view(request):
    return render(request, 'election_app/index.html')


def register_view(request):
    return render(request, 'election_app/register.html')


def login_view(request):
    return render(request, 'election_app/login.html')


def about_view(request):
    return render(request, 'election_app/about.html')


def contact_view(request):
    return render(request, 'election_app/contact.html')


def features_view(request):
    return render(request, 'election_app/features.html')
