from django.urls import path

from . import views

urlpatterns = [
    path('racks/', views.RacksListView.as_view(), name="racks_list"),
    path('racks/<str:slug>/', views.RacksDetailView.as_view(), name="racks_detail"),
    path('', views.BooksListView.as_view(), name="books_list"),
]