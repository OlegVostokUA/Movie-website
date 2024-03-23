from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/movielist', MovieAPIView.as_view()),
    path('', MovieList.as_view(), name='movie_list'),
    path('create/<str:arg>/', CreateNew.as_view(), name='create'),
    path('delete/<int:m_id>/', MovieDetail.as_view(), name='delete'),
    path('<int:pk>/update/', UpdateMovie.as_view(), name='update'),
    path('download-movie', DownloadFilms.as_view(), name='download_movies'),
    path('<slug:slug>/', MovieDetail.as_view(), name='movie_detail'),
    path('genre/<slug:genre_slug>/', MovieList.as_view(), name='movie_list_by_genre'),
    path('director/<slug:director_slug>/', MovieList.as_view(), name='movie_list_by_director'),
    path('actor/<slug:actor_slug>/', MovieList.as_view(), name='movie_list_by_actor'),
    path('year/<int:year>/', MovieList.as_view(), name='movie_list_by_year'),

]
