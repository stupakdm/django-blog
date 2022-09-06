from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about_blog'},
        {'title': 'Обо мне', 'url_name': 'about_me'},
        {'title': 'Проекты', 'url_name': 'blog'},
        {'title': 'Образование', 'url_name': 'education'},
        {'title': 'Обратная связь', 'url_name': 'response'},
        {'title': 'Редактировать', 'url_name': 'add_project'},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        places = cache.get('places')    #Достаем данные из кэша
        if not places:
            places = Places.objects.annotate(Count('projects'))
            cache.set('places', places, 60)     # Кладем данные в кэш

        user_menu = menu.copy()
        #if not self.request.user.is_authenticated:
        #    user_menu.pop(5)
        #else:
        #     user_menu.pop(6)

        context['menu'] = user_menu
        context['places'] = places
        if 'place_selected' not in context:
            context['place_selected'] = 0
        return context