from django.forms import ModelForm
from catalog.models import Book,Author,Genre,Language

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name','last_name', 'date_of_birth','date_of_death']


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','translator','language','translation','pub_year','condition','pur_date','genre','summary']


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name']
