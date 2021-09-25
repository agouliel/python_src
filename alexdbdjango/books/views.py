from django.shortcuts import render, redirect
from .models import Tblbook, Tblbookscateg
from .forms import CategForm

def index(request):
  return render(request, 'books/index.html')

def books(request):
  books = Tblbook.objects.order_by('title')
  context = {'books': books}
  return render(request, 'books/books.html', context)

def categories(request):
  categories = Tblbookscateg.objects.order_by('cdescr')
  context = {'categories': categories}
  return render(request, 'books/categories.html', context)

def category(request, cat_id):
  category = Tblbookscateg.objects.get(cid=cat_id)
  entries = category.tblbook_set.order_by('title')
  context = {'category': category, 'entries': entries}
  return render(request, 'books/category.html', context)

def new_cat(request):
  if request.method != 'POST':
    form = CategForm()
  else:
    form = CategForm(data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('books:categories')

  context = {'form': form}
  return render(request, 'books/new_cat.html', context)
