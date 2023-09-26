import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class FilmWork(UUIDMixin, TimeStampedMixin):

    class FilmWorkType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.TextField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creationdate'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    type = models.CharField(
        _('type'),
        max_length=7,
        choices=FilmWorkType.choices,
        blank=True,
        null=True,
    )
    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        blank=True,
        null=True,
    )
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre film work')
        verbose_name_plural = _('genre film works')
        constraints = [
            models.UniqueConstraint(fields=['genre', 'film_work'], name='unique film genre')
        ]


class Person(UUIDMixin, TimeStampedMixin):

    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.TextField(_('fullname'))
    film_works = models.ManyToManyField(FilmWork, through='PersonFilmWork')
    gender = models.TextField(
        _('gender'),
        choices=Gender.choices,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    class Role(models.TextChoices):
        WRITER = 'writer', _('writer')
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=Role.choices, default=Role.ACTOR)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person film work')
        verbose_name_plural = _('person film works')
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='unique person role in film')
        ]
