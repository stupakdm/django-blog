from django.contrib import admin
from django.contrib.gis import admin as gisAdmin
from django.utils.safestring import mark_safe

from .models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_project_created', 'get_html_image', 'is_finished', 'image', 'link')
    list_display_links = ('id', 'title', 'link')
    search_fields = ('title', 'content')
    list_editable = ('is_finished', )
    list_filter = ('is_finished', 'time_project_created')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'place', 'content', 'image', 'is_finished')
    readonly_fields = ('get_html_image',)
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")

    get_html_image.short_description = "Скриншоты"

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepolutated_fields = {"slug": ("name", )}

class PeopleAdmin(admin.ModelAdmin):
    list_display = ()

@gisAdmin.register(Marker)
class MarkerAdmin(gisAdmin.OSMGeoAdmin):

    list_display = ("name", "location")

admin.site.register(Projects, ProjectAdmin)
admin.site.register(Places, PlacesAdmin)

admin.site.site_title = 'Админ-панель сайта о моих проектах'
admin.site.site_header = 'Админ-панель сайта о моих проектах'
