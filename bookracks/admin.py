from django.contrib import admin
from django.contrib.admin import TabularInline

from . models import *

# Register your models here.


class BooksTabularInline(TabularInline):
    model = Book
    max_num = 10
    readonly_fields = ['slug']


class BookRacksAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_books', 'slug', 'created', 'modified')
    search_fields = ('name', 'slug', 'created', 'modified')
    date_hierarchy = 'created'
    readonly_fields = ('slug',)
    inlines = [
        BooksTabularInline
    ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','total_books', 'created', 'created', 'modified')
    search_fields = ('name',)
    readonly_fields = ('slug',)


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title','published_year',  'slug', 'created', 'modified')
    search_fields = ('title', 'slug', 'created', 'modified', 'author__name')
    list_filter = ('authors', 'published_year')
    date_hierarchy = 'created'
    readonly_fields = ('slug',)


admin.site.register(BookRack, BookRacksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BooksAdmin)