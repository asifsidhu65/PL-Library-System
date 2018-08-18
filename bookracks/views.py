from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from bookracks.models import BookRack, Book


class RacksListView(ListView):
    model = BookRack
    template_name = 'bookracks/racks/index.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RacksListView, self).get_context_data(object_list=None, **kwargs)
        return context


class RacksDetailView(DetailView):
    template_name = 'bookracks/racks/detail.html'
    model = BookRack


class BooksListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'bookracks/books/index.html'

    def get_queryset(self):
        query = super(BooksListView, self).get_queryset()
        qry = self.request.GET.get('search')
        if qry:
            query = query.filter(Q(title__contains=qry)|Q(published_year__contains=qry)|Q(authors__name__contains=qry))
            query = query.distinct()
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BooksListView, self).get_context_data(object_list=None, **kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context