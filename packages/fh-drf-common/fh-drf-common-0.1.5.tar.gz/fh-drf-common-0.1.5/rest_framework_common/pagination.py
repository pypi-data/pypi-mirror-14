from rest_framework.pagination import PageNumberPagination


class LargePageNumberPagination(PageNumberPagination):
    page_size = 100
