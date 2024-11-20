"""
URL configuration for election_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('admin/', admin.site.urls),
    # Route pour la page de connexion

    # Route pour la page d'index (page d'accueil)
    path('', views.index_view, name='index'),  # Vous devez ajouter cette vue dans votre fichier `views.py`

    path('register/', views.register_view, name='register'),

    path('about/', views.about_view, name='about'),

    path('login/', views.login_view, name='login'),

    path('contact/', views.contact_view, name='contact') ,

    path('features/', views.features_view, name='features'),

    path('help/', views.help_view, name='help'),
]
