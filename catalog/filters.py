from .models import Book
import django_filters

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title':['icontains',],
            'author':['exact',],
            'summary':['icontains',],
            'pub_year':['exact',],
            'owner':['exact',],
            'condition':['exact',],
            'language':['exact',],
            'translation':['exact',],
            'genre':['contains',],

            }
        