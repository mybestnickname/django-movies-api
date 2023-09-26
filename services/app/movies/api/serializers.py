from typing import List

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import FilmWork, PersonFilmWork


class FilmWorkSerializer(ModelSerializer):
    genres = SerializerMethodField()
    actors = SerializerMethodField()
    directors = SerializerMethodField()
    writers = SerializerMethodField()

    def create_people_list_by_role(self, obj: FilmWork, role: str) -> List:
        return [
            p_fw.person.full_name for p_fw in obj.personfilmwork_set.all()
            if p_fw.role == role
        ]

    def get_actors(self, obj):
        return self.create_people_list_by_role(obj, PersonFilmWork.Role.ACTOR)

    def get_directors(self, obj):
        return self.create_people_list_by_role(
            obj,
            PersonFilmWork.Role.DIRECTOR
        )

    def get_writers(self, obj):
        return self.create_people_list_by_role(obj, PersonFilmWork.Role.WRITER)

    def get_genres(self, obj):
        return [genre.name for genre in obj.genres.all()]

    class Meta:
        model = FilmWork
        fields = [
            'id', 'title', 'description',
            'creation_date', 'rating', 'type',
            'genres', 'actors', 'directors', 'writers'
        ]
