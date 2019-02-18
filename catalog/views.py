from django.shortcuts import render
from catalog.models import Book, Author,ReadingList,User
from django.views import generic
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from catalog.forms import BookForm,AuthorForm,GenreForm,LanguageForm

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




def add_book(request):
     
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
 
        form = BookForm()
 
        return render(request, "catalog/add_book.html", {'form': form})



def add_author(request):
     
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
 
        form = AuthorForm()
 
        return render(request, "catalog/add_author.html", {'form': form})

def add_genre(request):
     
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
 
        form = GenreForm()
 
        return render(request, "catalog/add_genre.html", {'form': form})

def add_language(request):
     
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
 
        form = LanguageForm()
 
        return render(request, "catalog/add_language.html", {'form': form})

from django.http import JsonResponse

def add_to_wish_list(request):
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)

    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))
    if ReadingList.objects.filter(reader=user_ins,book=book_ins).exists():
        data = {
            'status': 'Already in Wish List!'
            }
    elif ReadingList.objects.filter(reader=user_ins,book=book_ins,status='c').exists():
        data = {
            'status': 'Already Completed!'
            }
    elif ReadingList.objects.filter(reader=user_ins,book=book_ins,status='r').exists():
        data = {
            'status': 'Already Reading!'
            }

    else:
        item = ReadingList(reader=user_ins,book=book_ins,status='w')
        item.save()
        added = len(ReadingList.objects.filter(book=book_ins,reader=user_ins))!=0

        data = {
            'status': 'Added to Wish List!'
            }
    return JsonResponse(data)

def add_to_reading(request):
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)

    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))

    if ReadingList.objects.filter(reader=user_ins,book=book_ins,status='r').exists():
        data = {
            'status': 'Already Reading!'
            }
    elif ReadingList.objects.filter(reader=user_ins,book=book_ins,status='c').exists():
        data = {
            'status': 'Already Completed!'
            }
    else:
        wish_list_ins = ReadingList.objects.filter(reader=user_ins,book=book_ins,status='w')
        if wish_list_ins.exists():
            wish_list_ins.delete()
        item = ReadingList(reader=user_ins,book=book_ins,status='r')
        item.save()
        added = len(ReadingList.objects.filter(book=book_ins,reader=user_ins))!=0

        data = {
            'status': 'Added to Reading List!'
            }
    return JsonResponse(data)

def add_to_completed(request):    
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)

    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))

    if ReadingList.objects.filter(reader=user_ins,book=book_ins).exists():
        data = {
            'status': 'Already Completed!'
            }
    else:
        wish_list_ins = ReadingList.objects.filter(reader=user_ins,book=book_ins,status='w')
        if wish_list_ins.exists():
            wish_list_ins.delete()
        completed_ins = ReadingList.objects.filter(reader=user_ins,book=book_ins,status='c')
        if completed_ins.exists():
            completed_ins.delete()

        item = ReadingList(reader=user_ins,book=book_ins,status='c')
        item.save()
        added = len(ReadingList.objects.filter(book=book_ins,reader=user_ins))!=0

        data = {
            'status': 'Added to Completed!'
            }
    return JsonResponse(data)

def check_status(request):    
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)
    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))

    list_ins = ReadingList.objects.get(reader=user_ins,book=book_ins)
    if list_ins:
        data = {
            'status': list_ins.status
            }
    return JsonResponse(data)

