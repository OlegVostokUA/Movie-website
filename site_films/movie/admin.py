from django.contrib import admin
from .models import *


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}


class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name', )} # 'genre'



class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('first_name', 'last_name')}
    list_display = ['first_name', 'last_name']


class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('first_name', 'last_name')}
    list_display = ['first_name', 'last_name']


admin.site.register(Genre, GenreAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)

