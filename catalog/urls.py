from django.urls import path
from django.conf.urls import url
from django.urls import include, re_path
from . import views
from django_filters.views import FilterView
from catalog.filters import BookFilter

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
    template_name='catalog/result.html'), name='search'),    

    path('books/', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    ]