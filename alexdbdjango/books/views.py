from django.shortcuts import render
from .models import Tblbook

def index(request):
  return render(request, 'books/index.html')

def books(request):
  books = Tblbook.objects.order_by('title')
  context = {'books': books}
  return render(request, 'books/books.html', context)