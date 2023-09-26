from datetime import datetime

from django.urls.base import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from ..models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)


class FilmWorkListTest(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.genre_horror = baker.make(
            Genre,
            name='horror'
        )
        self.genre_sci_fi = baker.make(
            Genre,
            name='sci-fi'
        )
        self.genre_action = baker.make(
            Genre,
            name='action'
        )

        self.person_1 = baker.make(
            Person,
            full_name='person_1'
        )
        self.person_2 = baker.make(
            Person,
            full_name='person_2'
        )
        self.person_3 = baker.make(
            Person,
            full_name='person_3'
        )

        self.film_work_1 = baker.make(
            FilmWork,
            title='film_work_1',
            creation_date=datetime(2021, 11, 25),
            rating=8.7,
            type='movie'
        ) 
        self.film_work_2 = baker.make(
            FilmWork,
            title='film_work_2',
            creation_date=datetime(2021, 11, 26),
            rating=8.5,
        )
        self.film_work_3 = baker.make(
            FilmWork,
            title='film_work_3',
            creation_date=datetime(2021, 11, 27),
        )

        baker.make(
            GenreFilmWork,
            film_work=self.film_work_1,
            genre=self.genre_sci_fi,
        )
        baker.make(
            GenreFilmWork,
            film_work=self.film_work_1,
            genre=self.genre_horror,
        )

        baker.make(
            GenreFilmWork,
            film_work=self.film_work_2,
            genre=self.genre_sci_fi,
        )
        baker.make(
            GenreFilmWork,
            film_work=self.film_work_2,
            genre=self.genre_action,
        )

        baker.make(
            GenreFilmWork,
            film_work=self.film_work_3,
            genre=self.genre_horror,
        )
        baker.make(
            GenreFilmWork,
            film_work=self.film_work_3,
            genre=self.genre_action,
        )

        baker.make(
            PersonFilmWork,
            film_work=self.film_work_1,
            person=self.person_1,
            role='writer'
        )
        baker.make(
            PersonFilmWork,
            film_work=self.film_work_1,
            person=self.person_2,
            role='actor',
        )

        baker.make(
            PersonFilmWork,
            film_work=self.film_work_2,
            person=self.person_3,
            role='director'
        )
  
    def test_get_movies_list(self):
        response = self.client.get(f"{reverse('get_movies')}?genre=sci-fi")
        self.assertEqual(200, response.status_code)

        expected_result = {
            'count': 2,
            'total_pages': 1,
            'prev': None,
            'next': None,
            'results': [
                {
                    'id': str(self.film_work_1.id),
                    'title': self.film_work_1.title,
                    'description': self.film_work_1.description,
                    'creation_date': self.film_work_1.creation_date.strftime('%Y-%m-%d'),
                    'rating': self.film_work_1.rating,
                    'type': self.film_work_1.type,
                    'genres': [self.genre_horror.name, self.genre_sci_fi.name],
                    'actors': [self.person_2.full_name],
                    'directors': [],
                    'writers': [self.person_1.full_name]
                },
                {
                    'id': str(self.film_work_2.id),
                    'title': self.film_work_2.title,
                    'description': self.film_work_2.description,
                    'creation_date': self.film_work_2.creation_date.strftime('%Y-%m-%d'),
                    'rating': self.film_work_2.rating,
                    'type': None,
                    'genres': [self.genre_sci_fi.name, self.genre_action.name],
                    'actors': [],
                    'directors': [self.person_3.full_name],
                    'writers': []
                }
            ]
        }

        self.assertEqual(expected_result, response.data)


       
