# election_app/templatetags/election_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Renvoie la valeur correspondant à la clé dans le dictionnaire"""
    return dictionary.get(key)
