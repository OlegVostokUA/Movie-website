from django import forms
from .models import *


class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name',)


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ('first_name', 'last_name')


class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'director', 'actors', 'genre',
                  'description', 'year', 'country', 'poster')


class DownloadMovieForm(forms.Form):
    website = forms.CharField(label='Веб сайт')
    api_key = forms.CharField(label='Ключ API')
    movie_list = forms.CharField(label='Список фильмов', widget=forms.Textarea(attrs={'placeholder': 'Введите фильм или список фильмов разделенный запятыми'}))
