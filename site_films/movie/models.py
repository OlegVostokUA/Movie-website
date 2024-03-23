from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=20)
    url = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie:movie_list_by_genre', kwargs={'genre_slug': self.url})

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Actor(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    url = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('movie:movie_list_by_actor', kwargs={'actor_slug': self.url})

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Director(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    url = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('movie:movie_list_by_director', kwargs={'director_slug': self.url})

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'


class Movie(models.Model):
    name = models.CharField('Название', max_length=30)
    url = models.SlugField(max_length=30, unique=True)
    director = models.ManyToManyField(Director, verbose_name='режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актер', related_name='film_actor')
    genre = models.ManyToManyField(Genre, verbose_name='жанр', related_name='film_genre')
    description = models.TextField('Описание')
    year = models.PositiveIntegerField('Год')
    country = models.CharField('Страна', max_length=45)
    poster = models.ImageField('Постер', upload_to='movies/%Y/%m/%d')
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie:movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
