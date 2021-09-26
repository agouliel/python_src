from django.shortcuts import render, redirect
from .models import Tblbook, Tblbookscateg, Tblbookslocations, Tblbksites
from .forms import CategForm, LocForm, BookFromLocForm, BookFromCatForm, SiteForm, LocFromSiteForm, BookForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
  return render(request, 'books/index.html')

@login_required
def books(request):
  books = Tblbook.objects.filter(owner=request.user).order_by('title')
  context = {'books': books}
  return render(request, 'books/books.html', context)

################

def categories(request):
  categories = Tblbookscateg.objects.order_by('cdescr')
  context = {'categories': categories}
  return render(request, 'books/categories.html', context)

def category(request, cat_id):
  category = Tblbookscateg.objects.get(cid=cat_id)
  entries = category.tblbook_set.filter(owner=request.user).order_by('title')
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

################

def locations(request):
  locations = Tblbookslocations.objects.order_by('ldescr')
  context = {'locations': locations}
  return render(request, 'books/locations.html', context)

def location(request, loc_id):
  location = Tblbookslocations.objects.get(lid=loc_id)
  entries = location.tblbook_set.filter(owner=request.user).order_by('title')
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

def new_loc_from_site(request, site_id):
  site = Tblbksites.objects.get(sid=site_id)
  if request.method != 'POST':
    form = LocFromSiteForm()
  else:
    form = LocFromSiteForm(data=request.POST)
    if form.is_valid():
      new_loc_from_site = form.save(commit=False)
      new_loc_from_site.site = site
      new_loc_from_site.save()
      return redirect('books:site', site_id=site_id)
  context = {'site': site, 'form': form}
  return render(request, 'books/new_loc_from_site.html', context)

################

def new_book_from_cat(request, cat_id):
  category = Tblbookscateg.objects.get(cid=cat_id)
  if request.method != 'POST':
    form = BookFromCatForm()
  else:
    form = BookFromCatForm(data=request.POST)
    if form.is_valid():
      new_book_from_cat = form.save(commit=False)
      new_book_from_cat.category = category
      new_book_from_cat.owner = request.user
      new_book_from_cat.save()
      return redirect('books:category', cat_id=cat_id)
  context = {'category': category, 'form': form}
  return render(request, 'books/new_book_from_cat.html', context)

def new_book_from_loc(request, loc_id):
  location = Tblbookslocations.objects.get(lid=loc_id)
  if request.method != 'POST':
    form = BookFromLocForm()
  else:
    form = BookFromLocForm(data=request.POST)
    if form.is_valid():
      new_book_from_loc = form.save(commit=False)
      new_book_from_loc.location = location
      new_book_from_loc.owner = request.user
      new_book_from_loc.save()
      return redirect('books:location', loc_id=loc_id)
  context = {'location': location, 'form': form}
  return render(request, 'books/new_book_from_loc.html', context)

################

def sites(request):
  sites = Tblbksites.objects.order_by('sdescr')
  context = {'sites': sites}
  return render(request, 'books/sites.html', context)

def site(request, site_id):
  site = Tblbksites.objects.get(sid=site_id)
  entries = site.tblbookslocations_set.order_by('ldescr')
  context = {'site': site, 'entries': entries}
  return render(request, 'books/site.html', context)

def new_site(request):
  if request.method != 'POST':
    form = SiteForm()
  else:
    form = SiteForm(data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('books:sites')
  context = {'form': form}
  return render(request, 'books/new_site.html', context)

################

def new_book(request):
  if request.method != 'POST':
    form = BookForm()
  else:
    form = BookForm(data=request.POST)
    if form.is_valid():
      new_book = form.save(commit=False)
      new_book.owner = request.user
      new_book.save()
      return redirect('books:books')
  context = {'form': form}
  return render(request, 'books/new_book.html', context)

def edit_book(request, book_id):
  book = Tblbook.objects.get(bid=book_id)
  if book.owner != request.user:
    raise Http404
  if request.method != 'POST':
    # pre-fill form with the current book
    form = BookForm(instance=book)
  else:
    form = BookForm(instance=book, data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('books:books')
  context = {'book': book, 'form': form}
  return render(request, 'books/edit_book.html', context)

class DeleteMe(DeleteView):
    template_name = 'books/deleteconfirmation.html'
    model = Tblbook
    success_url = '/books/' # or reverse_lazy
