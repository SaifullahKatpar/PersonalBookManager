from django.forms import ModelForm
from catalog.models import Book,Author,Genre,Language,ReadingList
from django import forms

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name','last_name', 'date_of_birth','date_of_death']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class':'datepicker'}),
            'date_of_death': forms.DateInput(attrs={'class':'datepicker'}),
        }


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','translator','language','translation','pub_year','condition','pur_date','genre','archive','summary']
        widgets = {
            'pur_date': forms.DateInput(attrs={'class':'datepicker'}),
        }


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name']

    def clean_name(self):
        from django.core.exceptions import ValidationError
        name = self.cleaned_data['name']
        if Language.objects.filter(name__iexact=name).exists():
            raise ValidationError("Already exists!")
        return name

