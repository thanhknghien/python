# bookstore/urls.py
from django.urls import path
from .views.customer import home

urlpatterns = [
    path('', home.home, name='home'),
    path('books/', home.books, name='books'),
]