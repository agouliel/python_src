"""Books URL Configuration"""

from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:cat_id>', views.category, name='category'),
    path('new_cat/', views.new_cat, name='new_cat'),
]