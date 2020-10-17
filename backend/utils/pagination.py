from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"code": 200, "msg": None, "data": OrderedDict([
            ('page', self.page.number),
            ('page_size', self.page.paginator.per_page),
            ('total_size', self.page.paginator.count),
            ('total_page', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
            ('content', data)
        ])})
