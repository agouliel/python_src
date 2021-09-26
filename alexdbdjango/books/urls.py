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

    path('locations/', views.locations, name='locations'),
    path('locations/<int:loc_id>', views.location, name='location'),
    path('new_loc/', views.new_loc, name='new_loc'),

    path('new_book_from_cat/<int:cat_id>', views.new_book_from_cat, name='new_book_from_cat'),
    path('new_book_from_loc/<int:loc_id>', views.new_book_from_loc, name='new_book_from_loc'),

    path('sites/', views.sites, name='sites'),
    path('sites/<int:site_id>', views.site, name='site'),
    path('new_site/', views.new_site, name='new_site'),
    path('new_loc/<int:site_id>', views.new_loc_from_site, name='new_loc_from_site'),

    path('new_book/', views.new_book, name='new_book'),
    path('edit_book/<int:book_id>', views.edit_book, name='edit_book'),
    path('deleteurl/<int:pk>', views.DeleteMe.as_view(), name='deletemeview'),
]