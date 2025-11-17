# login/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Access dictionary items using key."""
    return dictionary.get(key)


@register.filter(name='dict_get')
def dict_get(dictionary, key):
    """Returns the value of the key from dictionary or None if key doesn't exist"""
    return dictionary.get(key) if dictionary else None
