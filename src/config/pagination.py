from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ResponsePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'current_page': self.page.number,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
                'count': self.page.paginator.count,
            },
            'results': data,
        })
