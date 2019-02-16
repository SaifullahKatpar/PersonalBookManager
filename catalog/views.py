from django.shortcuts import render
from catalog.models import Book, Author
from django.views import generic

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
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