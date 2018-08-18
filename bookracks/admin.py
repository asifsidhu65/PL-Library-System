from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Count
from django.forms import ModelChoiceField

from . models import *

# Register your models here.


class BooksTabularInline(TabularInline):
    model = Book
    max_num = 10
    extra = 1
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'book_rack':
            query_set = BookRack.objects.annotate(num_books=Count('book')).filter(num_books__lt=10)
            return ModelChoiceField(query_set)
        return super(BooksAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(BookRack, BookRacksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BooksAdmin)