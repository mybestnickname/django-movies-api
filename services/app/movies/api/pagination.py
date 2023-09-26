from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FilmWorkPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': self.page.previous_page_number() if self.page.has_previous() else None,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'results': data,
        })
