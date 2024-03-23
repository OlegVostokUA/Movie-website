import requests
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import UpdateView
from pytils.translit import slugify
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .serializer import *
from .forms import *


class MovieList(View):
    def get(self, request, genre_slug=None, director_slug=None, actor_slug=None, year=None):
        genres = Genre.objects.all()
        movies = Movie.objects.all()
        directors = Director.objects.all()
        actors = Actor.objects.all()

        years = []
        for i in movies:
            years.append(i.year)
        years = set(years)
        years = list(years)
        years.sort()

        if genre_slug:
            genre = get_object_or_404(Genre, url=genre_slug)
            movies = movies.filter(genre=genre)
        if director_slug:
            director = get_object_or_404(Director, url=director_slug)
            movies = movies.filter(director=director)
        if actor_slug:
            actor = get_object_or_404(Actor, url=actor_slug)
            movies = movies.filter(actors=actor)
        if year:
            movies = movies.filter(year=year)

        # pagination
        paginator = Paginator(movies, 8)
        page = request.GET.get('page')
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        return render(request, 'movie_list.html', {'movies': movies,
                                                   'genres': genres,
                                                   'directors': directors,
                                                   'actors': actors,
                                                   'years': years,
                                                   'page': page})


class MovieDetail(View):
    def get(self, request, slug=None, m_id=None):
        if m_id:
            movie = get_object_or_404(Movie, id=m_id)
            movie.delete()
            return redirect('movie:movie_list')

        movie = Movie.objects.get(url=slug)
        return render(request, 'movie_detail.html', {'movie': movie})


class CreateNew(View):
    def get(self, request, arg=None):
        form = None
        if arg == 'genre':
            form = AddGenreForm()
        elif arg == 'actor' or arg == 'director':
            form = AddPersonForm()
        elif arg == 'movie':
            form = AddMovieForm()

        return render(request, 'create/create.html', {'form': form,
                                                      'arg': arg})

    def post(self, request=None, arg=None):
        form = None
        if arg == 'genre':
            form = AddGenreForm(request.POST)
            if form.is_valid():
                new_genre = form.save(commit=False)
                new_slug = slugify(new_genre)
                Genre.objects.create(name=new_genre, url=new_slug)
                return render(request, 'create/created.html', { 'title_item': arg,
                                                                'new_item': new_genre})
        elif arg == 'actor' or arg == 'director':
            form = AddPersonForm(request.POST)
            if form.is_valid():
                f_name = form.cleaned_data.get("first_name")
                l_name = form.cleaned_data.get("last_name")
                slug = slugify(f_name+'-'+l_name)
                if arg == 'actor':
                    Actor.objects.create(first_name=f_name, last_name=l_name, url=slug)
                elif arg == 'director':
                    Director.objects.create(first_name=f_name, last_name=l_name, url=slug)
                return render(request, 'create/created.html', { 'title_item': arg,
                                                                'new_item': f_name,
                                                                'new_item_2': l_name})
        elif arg == 'movie':
            form = AddMovieForm(request.POST, request.FILES)
            if form.is_valid():
                movie = Movie()
                name = form.cleaned_data.get('name')
                movie.name = name
                movie.url = slugify(name)
                director = form.cleaned_data.get('director')
                actors = form.cleaned_data.get('actors')
                genre = form.cleaned_data.get('genre')
                movie.description = form.cleaned_data.get('description')
                movie.year = form.cleaned_data.get('year')
                movie.country = form.cleaned_data.get('country')
                movie.poster = form.cleaned_data.get('poster')
                movie.draft = False
                movie.save()
                movie.director.set(director)
                movie.actors.set(actors)
                movie.genre.set(genre)
                return render(request, 'create/created.html', { 'title_item': arg,
                                                                'new_item': name})


class UpdateMovie(UpdateView):
    model = Movie
    template_name = 'create/create.html'
    form_class = AddMovieForm


# classes for API work
class MovieAPIView(APIView):
    def get(self, request):
        list_films = Movie.objects.all()
        list_actors = Actor.objects.all()
        list_directors = Director.objects.all()
        list_genres = Genre.objects.all()

        serializer_class_movie = MovieSerializer(list_films, many=True)
        serializer_class_actor = ActorSerializer(list_actors, many=True)
        serializer_class_director = DirectorSerializer(list_directors, many=True)
        serializer_class_genre = GenreSerializer(list_genres, many=True)

        return Response({'genres': serializer_class_genre.data,
                         'films': serializer_class_movie.data,
                         'actors': serializer_class_actor.data,
                         'directors': serializer_class_director.data})


class DownloadFilms(View):
    def get(self, request):
        form = DownloadMovieForm()
        return render(request, 'download/download.html', {'form': form})

    def post(self, request):
        form = DownloadMovieForm(request.POST, request.FILES)
        if form.is_valid():
            website = form.cleaned_data.get("website")
            api_key = form.cleaned_data.get("api_key")
            movie_list = form.cleaned_data.get("movie_list").split(', ')
            for mov in movie_list:
                params = dict(apikey=api_key, t=mov)
                result_json = requests.get(url=website, params=params).json()
                # genre add
                genres_new_film = result_json['Genre'].split(', ')
                for genre in genres_new_film:
                    genre_slug = slugify(genre)
                    genre_in_db = Genre.objects.filter(url=genre_slug)
                    if not genre_in_db:
                        Genre.objects.create(name=genre, url=genre_slug)
                # actors add
                actors_new_film = result_json['Actors'].split(', ')
                for actor in actors_new_film:
                    actor_slug = slugify(actor)
                    actor_f_name_l_name = actor.split(' ')
                    actor_in_db = Actor.objects.filter(url=actor_slug)
                    if not actor_in_db:
                        Actor.objects.create(first_name=actor_f_name_l_name[0], last_name=actor_f_name_l_name[1], url=actor_slug)
                # directors add
                directors_new_film = result_json['Director'].split(', ')
                for director in directors_new_film:
                    director_slug = slugify(director)
                    director_f_name_l_name = director.split(' ')
                    director_in_db = Director.objects.filter(url=director_slug)
                    if not director_in_db:
                        Director.objects.create(first_name=director_f_name_l_name[0], last_name=director_f_name_l_name[1], url=director_slug)
                # movie add
                movie = Movie()
                name = result_json['Title']
                movie.name = name
                movie.url = slugify(name)
                movie.description = result_json['Plot']
                movie.year = result_json['Year']
                movie.country = result_json['Country']
                movie.poster = result_json['Poster'] # poster not aviable on this API
                movie.poster = '/default.jpg' # default poster ^^^
                movie.draft = False
                movie.save()
                qs_genre = Genre.objects.filter(url='default_none')
                qs_actors = Actor.objects.filter(url='default_none')
                qs_directors = Director.objects.filter(url='default_none')
                for genre in genres_new_film:
                    genre_to_film = Genre.objects.filter(url=slugify(genre))
                    qs_genre = qs_genre.union(genre_to_film)
                for actor in actors_new_film:
                    actor_to_film = Actor.objects.filter(url=slugify(actor))
                    qs_actors = qs_actors.union(actor_to_film)
                for director in directors_new_film:
                    director_to_film = Director.objects.filter(url=slugify(director))
                    qs_directors = qs_directors.union(director_to_film)
                movie.genre.set(qs_genre)
                movie.actors.set(qs_actors)
                movie.director.set(qs_directors)
            return render(request, 'download/downloaded.html')
