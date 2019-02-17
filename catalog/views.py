from django.shortcuts import render
from catalog.models import Book, Author,ReadingList
from django.views import generic
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    num_genres = Book.objects.all().aggregate(Count('genre',distinct=True))  
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_genres': num_genres['genre__count'],
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

from django.views import View


from .filters import BookFilter

class SearchListView(generic.ListView):
    model = Book
    template_name = "catalog/result.html"

    def get_context_data(self,**kwargs):
        context = super.get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET,queryset=self.get_queryset())
        return context
def search(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'catalog/result.html', {'filter': book_filter})

class ReadingListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = ReadingList
    template_name ='catalog/book_list_reading_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return ReadingList.objects.filter(reader=self.request.user)

class NewBooksListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Book
    template_name ='catalog/new_arrivals.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Book.objects.all()