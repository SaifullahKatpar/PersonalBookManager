from django.db import models

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

import datetime
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    LANGUAGES = (
        ('e', 'English'),
        ('u', 'Urdu'),
        ('s', 'Sindhi'),
        ('a', 'Arabic'),
        ('p', 'Persion'),
    )
    CONDITIONS = (
        ('g','Good'),
        ('b','Bad'),
        ('f','fine'),
    )
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=1,choices = LANGUAGES,blank=True, default='s')
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    YEAR_CHOICES = [(r,r) for r in range(1800, datetime.date.today().year+1)]
    pub_year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    condition = models.CharField(max_length=1,choices = CONDITIONS,blank=True, default='g')
    class Meta:
        ordering = ['title','-pub_year']

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name','last_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
        