from django.shortcuts import render,HttpResponse
from catalog.models import Book, Author, Genre, Language,    ReadingList,User
from django.views import generic
from rest_framework import generics
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
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['books'] = Book.objects.filter(author=self.object.pk) | Book.objects.filter(translator=self.object.pk)

            return context

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

from datetime import date, timedelta

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
    from django.core.exceptions import ValidationError
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

        data = {
            'status': 'Added to Reading List!'
            }
    return JsonResponse(data)

def add_to_completed(request):    
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)

    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))

    if ReadingList.objects.filter(reader=user_ins,book=book_ins,status='w').exists():
        data = {
            'status': 'You have not read this book!'
            }
    elif ReadingList.objects.filter(reader=user_ins,book=book_ins,status='r'):
        reading_ins = ReadingList.objects.filter(reader=user_ins,book=book_ins,status='r')
        reading_ins.delete()

        item = ReadingList(reader=user_ins,book=book_ins,status='c')
        item.save()

        data = {
            'status': 'Added to Completed!'
            }
    else:
        data = {
            'status': 'No action performed!'
            }

    return JsonResponse(data)

def check_status(request):    
    id_book = request.GET.get('id_book', None)
    id_user = request.GET.get('id_user', None)
    book_ins = Book.objects.get(id=int(id_book))
    user_ins = User.objects.get(id=int(id_user))

    if ReadingList.objects.filter(reader=user_ins,book=book_ins).exists():
        list_ins = ReadingList.objects.get(reader=user_ins,book=book_ins)
        data = {
            'status': list_ins.status
            }
    else:
        data = {
            'status': 'No Status'
            }
    return JsonResponse(data)



from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, LanguageSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LanguageList(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer



