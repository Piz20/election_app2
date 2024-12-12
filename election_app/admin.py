from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Election, Candidate, Vote


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'matricule', 'gender', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'gender')
    search_fields = ('email', 'name', 'matricule')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'matricule', 'gender', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

# Election Admin
class ElectionAdmin(admin.ModelAdmin):
    model = Election
    list_display = ('name', 'start_date', 'end_date',)
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)

# Candidate Admin
class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    list_display = ('name', 'election', 'vote_count')
    search_fields = ('name', 'election__name')
    list_filter = ('election',)
    ordering = ('election', 'name')


class VoteAdmin(admin.ModelAdmin):
    # Définir les champs à afficher dans la liste des votes
    list_display = ('user', 'candidate',)

    # Ajouter des filtres dans la barre latérale pour filtrer les votes
    list_filter = ('candidate__election', 'user')

    # Ajouter une barre de recherche pour rechercher par utilisateur ou candidat
    search_fields = ('user__email', 'candidate__name')

    # Autoriser l'édition des votes directement depuis la liste
    list_editable = ('candidate',)


# Enregistrer le modèle avec la classe d'administration personnalisée
admin.site.register(Vote, VoteAdmin)
# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
