from django import template

from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active_handler(context, page, **kwargs):
    if reverse(page) in context.request.path:
        return mark_safe("active")


# @register.filter
# def countdown(date):
#     timeremaining = date.replace(tzinfo=None) - datetime.now()
#
#     s = (int)(timeremaining.total_seconds())
#     hours = s // 3600
#     s = s - hours * 3600
#     minutes = s // 60
#     seconds = s - (minutes * 60)
#
#     return '%02d:%02d:%02d' % (hours, minutes, seconds)
#
#
# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)
#
#
# @register.filter
# def order_by(things, order):
#     return things.order_by(order)
