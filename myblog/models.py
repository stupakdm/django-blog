from django.db import models
from django.urls import reverse
from django.contrib.gis.db.models import PointField


class Projects(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название проекта')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Описание проекта')
    time_project_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания проекта')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_finished = models.BooleanField(default=True, verbose_name='Завершение проекта')
    link = models.URLField(max_length=255, blank=True, verbose_name='Ссылка')
    image = models.ImageField(verbose_name='Скриншот проекта', upload_to="photos/%T/")   #Topic/number
    place = models.ForeignKey('Places', on_delete=models.PROTECT, verbose_name='Периоды')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_info', kwargs={'project_slug': self.slug})

    class Meta:
        verbose_name = 'Мои проекты'
        verbose_name_plural = 'Мои проекты'
        ordering = ['time_project_created', 'is_finished', 'title']

class Places(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Период")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('places', kwargs={'place_slug': self.slug})

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
        ordering = ['id']

class AboutInfo(models.Model):
    name = models.CharField(max_length=255, verbose_name='Дмитрий Ступак')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    age = models.IntegerField(verbose_name='Возраст')
    date_time = models.DateField(auto_now_add=True, verbose_name='Дата рождения')
    content = models.TextField(blank=True, verbose_name='Биография')
    image = models.ImageField(verbose_name='Фото', upload_to="photos/%T/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обо мне'

class TextInfo(models.Model):
    text = models.TextField(blank=True, verbose_name='Для чего этот сайт')
    link_projects = models.URLField(max_length=255, blank=True, verbose_name='Ссылка на проекты')
    link_biography = models.URLField(max_length=255, blank=True, verbose_name='Ссылка на биографию')
    link_reply = models.URLField(max_length=255, blank=True, verbose_name='Ссылка на ответ')

    #def __str__(self):
    #    return self.name

    class Meta:
        verbose_name = 'О сайте'

class Marker(models.Model):

    name = models.CharField(max_length=255, verbose_name='Университет')
    location = PointField()