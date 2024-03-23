from rest_framework import serializers
from .models import Movie, Director, Actor, Genre


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        #fields = ("name", "url", "director", "actors", "genre", "description", "country", "poster", "draft")
        fields = "__all__"

        def create(self, validated_data):
            print('save meth ser class')
            #GenreSerializer.save(validated_data)
            return Movie.objects.create(**validated_data)




class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        #fields = ("name", "director", "actors", "genre", "description", "country")
        fields = "__all__"

        def create(self, validated_data):
            return Director.objects.create(**validated_data)

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        #fields = ("name", "director", "actors", "genre", "description", "country")
        fields = "__all__"

        def create(self, validated_data):
            return Actor.objects.create(**validated_data)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        #fields = ("name", "url")
        fields = "__all__"

        def create(self, validated_data):
            print('create genre', validated_data)
            return Genre.objects.create(**validated_data)

"""
{'name': 'Film 1 test', 'url': 'film-1-test-2', 'description': 'test film description', 'country': 'test country', 'poster': '/movies/2024/02/28/%D0%9D%D0%BE%D0%B2%D1%8B%D0%B9_%D1%82%D0%BE%D1%87%D0%B5%D1%87%D0%BD%D1%8B%D0%B9_%D1%80%D0%B8%D1%81%D1%83%D0%BD%D0%BE%D0%BA.bmp', 'draft': False, 'director': [1], 'actors': [1], 'genre': [2]}
"""
