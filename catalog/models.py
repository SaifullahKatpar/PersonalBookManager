from django.db import models
from django.contrib.auth.models import User    
from datetime import date, timedelta
# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)',unique=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

import datetime
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    CONDITIONS = (
        ('g','Good'),
        ('b','Bad'),
        ('f','fine'),
    )
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author',  related_name="author",on_delete=models.SET_NULL, null=True)
    translator = models.ForeignKey('Author', related_name="translator",on_delete=models.SET_NULL, null=True,blank=True)
    language = models.ForeignKey('Language',related_name="language", on_delete=models.SET_NULL, null=True)
    translation = models.ForeignKey('Language', related_name="translation",on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    YEAR_CHOICES = [(r,r) for r in range(1800, datetime.date.today().year+1)]
    pub_year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    condition = models.CharField(max_length=1,choices = CONDITIONS,blank=True, default='g')
    pur_date = models.DateField(null=True, blank=True, help_text='Date in Year-Month-Date')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    archive =  models.BooleanField(default=False, help_text='In store')
    @property
    def is_new(self):
        if self.pur_date and self.pur_date+ timedelta(days=30) >= date.today()  :
            return True
        return False
    new_arrival = property(is_new)
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
        return f'{self.first_name} {self.last_name}'

class ReadingList(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    @property
    def is_reading(self):
        if self.status=='r':
            return True
        return False
    @property
    def is_completed(self):
        if self.status=='c':
            return True
        return False
    @property
    def is_wish(self):
        if self.status=='w':
            return True
        return False


    STATUS = (
        ('r', 'Reading'),
        ('c', 'Completed'),
        ('w', 'Wish List'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='w',
        help_text='Reading List')

    class Meta:
        ordering = ['book']

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.book.title)

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",unique=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


