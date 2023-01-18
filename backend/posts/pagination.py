from rest_framework.pagination import CursorPagination

class StandardResultsSetPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 40
    ordering = [
        '-created_at',
    ]