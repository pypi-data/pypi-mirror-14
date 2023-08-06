from django import template
from django.utils import timezone

from ..models import Event

register = template.Library()


@register.assignment_tag
def get_upcoming_events(count=5, category=None):
    event_list = Event.objects.published().filter(start__gt=timezone.now())

    # Optional filter by category
    if category is not None:
        event_list = event_list.filter(category__slug=category)

    return event_list[:count]
