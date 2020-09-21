from django import template
from django.http import QueryDict


register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.name in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.name)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.name)
    return new_request.urlencode()
