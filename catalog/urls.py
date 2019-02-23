from django.urls import path
from django.conf.urls import url
from django.urls import include, re_path
from . import views
from django_filters.views import FilterView
from catalog.filters import BookFilter
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^search/$', FilterView.as_view(filterset_class=BookFilter,
    template_name='catalog/result.html'), name='search'),    

    path('books/', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    ]

urlpatterns += [   
    path('mybooks/', views.ReadingListView.as_view(), name='reading_list'),
]

urlpatterns += [   
    path('add_book/', login_required(views.add_book), name='add_book'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('add_language/', views.add_language, name='add_language'),
]

urlpatterns += [
    path('add_to_wish_list/', views.add_to_wish_list, name='add_to_wish_list'),
    path('add_to_reading/', views.add_to_reading, name='add_to_reading'),
    path('add_to_completed/', views.add_to_completed, name='add_to_completed'),
    path('check_status/', views.check_status, name='check_status'),
]
