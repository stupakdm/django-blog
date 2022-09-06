from django import template
from myblog.models import *

register = template.Library()

@register.simple_tag(name='getplaces')
def get_places(filter=None):
    if not filter:
        return Places.objects.all()
    else:
        return Places.objects.filter(pk=filter)

@register.inclusion_tag('myblog/list_places.html')
def show_places(sort = None, place_selected=0):
    if not sort:
        places = Places.objects.all()
    else:
        places = Places.objects.order_by(sort)
    return {'places': places, 'place_selected': place_selected}