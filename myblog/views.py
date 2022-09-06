import json

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .forms import *
from .models import *
from .utils import *

class ProjectsHome(DataMixin, ListView):
    paginate_by = 1  # Paginator
    model = Projects
    template_name = 'myblog/index.html'
    context_object_name = 'projects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items())+list(c_def.items()))
        return context

    def get_queryset(self):
        return Projects.objects.all().select_related('place')
        #return Projects.objects.filter(is_finished=True)
"""def blog(request):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    projects = Projects.objects.all()

    context = {
        'projects': projects.order_by('time_project_created'),
        'menu': menu,
        'title': 'Главная страница блога',
        'place_selected': 0,
    }
    # projects = projects.order_by('time_project_created')
    #return reverse(request, 'myblog/index.html')
    return render(request, 'myblog/index.html', context=context)#context=context)
"""

class ProjectInfo(DataMixin, DetailView):
    model = Projects
    template_name = 'myblog/project.html'
    slug_url_kwarg = 'project_slug'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['project'].title)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

"""def project_info(request, project_slug):
    project = get_object_or_404(Projects, slug=project_slug)

    context = {
        'project': project,
        'menu': menu,
        'title': project.title,
        'place_selected': project.place_id,
    }
    return render(request, 'myblog/project.html', context=context)"""
#def project_info(request, project_id):
#    return HttpResponse(f"Отображение проекта {project_id}")


#@login_required
def about_me(request):
    people = AboutInfo.objects.all()
    #contact_list = Projects.objects.all()
    #paginator = Paginator(contact_list, 3)

    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    return render(request, 'myblog/about.html', {'menu': menu, 'people': people})#{'myself': myself})

#@login_required
def about_blog(request):
    blog = TextInfo.objects.get(id = 1)
    #paginator = Paginator(contact_list, 3)

    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    return render(request, 'myblog/about_blog.html', {'menu': menu, 'this_blog':blog})


def projects(request, proj_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h2>Проекты</h2><p>{proj_id}</p>")

class EducationMapView(DataMixin, TemplateView):
    template_name = "myblog/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Образование')
        context = dict(list(context.items()) + list(c_def.items()))
        context["markers"] = json.loads(serialize("geojson", Marker.objects.all()))
        return context


def education(request, year=2022):
    if int(year) > 2022 or int(year) < 2010:
        return redirect('blog', permanent=True)
    # if request.POST:

    return render(request, 'myblog/education.html', {'menu':menu, 'year': year})
    #return HttpResponse(f"<h2>Университет</h2><p>{year}</p>")


def university(request, year=2022):
    if int(year) > 2022 or int(year) < 2010:
        return redirect('blog', permanent=True)
    # if request.POST:

    return HttpResponse(f"<h2>Университет</h2><p>{year}</p>")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'myblog/response.html'
    success_url = reverse_lazy('blog')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('blog')
#def response(request):
#    return render(request, 'myblog/response.html')


#def login(request):
#    return render(request, 'myblog/login.html')


class AddProject(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "myblog/add_project.html"
    success_url = reverse_lazy('blog')
    login_url = reverse_lazy('blog')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

"""def add_project(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            #try:
                #Projects.objects.create(**form.cleaned_data)
                form.save()
                return redirect('blog')
            #except:
            #    form.add_error(None, 'Ошибка добавления проекта')
    else:
        form = AddPostForm()
    return render(request, 'myblog/add_project.html', {'form': form, 'menu': menu, 'title': 'Добавление проекта'})
"""

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ProjectsPlace(DataMixin, ListView):
    model = Projects
    template_name = 'myblog/index.html'
    context_object_name = 'projects'
    allow_empty = False

    def get_queryset(self):
        return Projects.objects.filter(place__slug=self.kwargs['place_slug']).select_related('place')
        #return Projects.objects.filter(place__slug=self.kwargs['place_slug'], is_finished=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Places.objects.get(slug=self.kwargs['place_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(context['projects'][0].place), place_selected=c.pk)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'myblog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('blog')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'myblog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('blog')

def logout_user(request):
    logout(request)
    return redirect('login')
"""def show_places(request, place_id):
    projects = Projects.objects.filter(place_id=place_id)

    context = {
        'projects': projects.order_by('time_project_created'),
        'menu': menu,
        'title': 'Главная страница блога',
        'place_selected': place_id,
    }
    return render(request, 'myblog/index.html', context=context)"""