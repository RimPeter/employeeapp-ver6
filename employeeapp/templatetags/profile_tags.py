from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def get_user_profile(user):
    try:
        return user.profile
    except ObjectDoesNotExist:
        return None
