from django.urls import path

from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.FilmWorkListView.as_view(), name='get_movies'),
    path('movies/<uuid:id>', views.FilmWorkView.as_view(), name='get_movie'),
]