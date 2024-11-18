# projet/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def index_view():
    return redirect('login')  # Redirige vers la page de login par défaut

urlpatterns = [
    path('', index_view),  # Redirection vers la page de login par défaut
    path('admin/', admin.site.urls),
    path('election/', include('election_app.urls')),
]
