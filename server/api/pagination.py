from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  #default size
    page_size_query_param = 'size'
    max_page_size = 20

