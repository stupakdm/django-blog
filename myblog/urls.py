from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.urls import path, re_path

from blog import settings
from .views import *

urlpatterns = [
    path('s2pak/', cache_page(60)(ProjectsHome.as_view()), name='blog'),
    path('about_me/', about_me, name='about_me'),
    path('about_blog/', about_blog, name='about_blog'),
    path('education/', EducationMapView.as_view(), name='education'),
    path("projects/<int:proj_id>/", projects, name='projects'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user,name='logout'),
    path('response/', ContactFormView.as_view(), name='response'),
    path('add_project/', AddProject.as_view(), name='add_project'),
    path('s2pak/<slug:project_slug>/', ProjectInfo.as_view(), name='project_info'),
    path('places/<slug:place_slug>/', ProjectsPlace.as_view(), name='places'),
    re_path(r'^university/(?P<year>[0-9]{4})/', university, name='university'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = pageNotFound