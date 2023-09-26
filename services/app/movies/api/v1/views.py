from movies.models import FilmWork
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from ..pagination import FilmWorkPagination
from ..serializers import FilmWorkSerializer


class FilmWorkListView(generics.ListAPIView):
    serializer_class = FilmWorkSerializer
    model = serializer_class.Meta.model
    pagination_class = FilmWorkPagination

    def get_queryset(self):
        queryset = (
            FilmWork.objects
            .prefetch_related(
                "genres",
                "personfilmwork_set__person"
            )
            .order_by('creation_date')
            .all()
        )

        genre = self.request.query_params.get('genre')
        if genre is not None:
            if genre:
                queryset = queryset.filter(genres__name=genre)
            else:
                raise ValidationError("empty genre param")
        return queryset


class FilmWorkView(generics.RetrieveAPIView):
    serializer_class = FilmWorkSerializer
    lookup_field = 'id'
    queryset = (
        FilmWork.objects
        .prefetch_related(
            "genres",
            "personfilmwork_set__person"
        )
        .all()
    )
