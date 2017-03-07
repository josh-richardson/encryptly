from django import template

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active_handler(context, page, **kwargs):
    if reverse(page) in context.request.path:
        return mark_safe("active")
