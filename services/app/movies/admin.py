from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Genre,
    FilmWork,
    GenreFilmWork,
    Person,
    PersonFilmWork
)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork

    autocomplete_fields = ['person']


class NotChangeablePersonFilmWorkInline(PersonFilmWorkInline):

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (NotChangeablePersonFilmWorkInline,)

    list_filter = ('gender',)

    search_fields = ('full_name', 'film_works__title')

    ordering = ('full_name',)

    list_display = ('full_name', 'gender')

    search_help_text = _(
        'You can search by actor name or film title.'
    )  # (New in Django 4.0.)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating',)

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')
