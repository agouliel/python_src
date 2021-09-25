from django.shortcuts import render, redirect
from .models import Tblbook, Tblbookscateg, Tblbookslocations
from .forms import CategForm, LocForm, BookForm

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

def locations(request):
  locations = Tblbookslocations.objects.order_by('ldescr')
  context = {'locations': locations}
  return render(request, 'books/locations.html', context)

def location(request, loc_id):
  location = Tblbookslocations.objects.get(lid=loc_id)
  entries = location.tblbook_set.order_by('title')
  context = {'location': location, 'entries': entries}
  return render(request, 'books/location.html', context)

def new_loc(request):
  if request.method != 'POST':
    form = LocForm()
  else:
    form = LocForm(data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('books:locations')
  context = {'form': form}
  return render(request, 'books/new_loc.html', context)

def new_book_from_cat(request, cat_id):
  category = Tblbookscateg.objects.get(cid=cat_id)
  if request.method != 'POST':
    form = BookForm()
  else:
    form = BookForm(data=request.POST)
    if form.is_valid():
      new_book_from_cat = form.save(commit=False)
      new_book_from_cat.category = category
      new_book_from_cat.save()
      return redirect('books:category', cat_id=cat_id)
  context = {'category': category, 'form': form}
  return render(request, 'books/new_book_from_cat.html', context)

def new_book_from_loc(request, loc_id):
  location = Tblbookslocations.objects.get(lid=loc_id)
  if request.method != 'POST':
    form = BookForm()
  else:
    form = BookForm(data=request.POST)
    if form.is_valid():
      new_book_from_loc = form.save(commit=False)
      new_book_from_loc.location = location
      new_book_from_loc.save()
      return redirect('books:location', loc_id=loc_id)
  context = {'location': location, 'form': form}
  return render(request, 'books/new_book_from_loc.html', context)
