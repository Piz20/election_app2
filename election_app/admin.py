from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Election, Candidate

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
    list_display = ('name', 'start_date', 'end_date', 'winner')
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

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
