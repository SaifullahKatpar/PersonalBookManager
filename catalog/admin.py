from django.contrib import admin
from catalog.models import Author, Genre, Book, ReadingList


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    
admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'reader')
    list_filter = ('book',)
    
    fieldsets = (
        (None, {
            'fields': ('book',)
        }),
        ('Reading', {
            'fields': ('status','reader',)
        }),
    )