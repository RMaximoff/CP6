from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def mediapath(value):
    return f"/media/{value}"


@register.filter()
def is_moderator(user):
    return user.groups.filter(name='moderators').exists()
