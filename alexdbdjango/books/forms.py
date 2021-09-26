from django import forms
from .models import Tblbookscateg, Tblbookslocations, Tblbksites, Tblbook

class CategForm(forms.ModelForm):
  class Meta:
    model = Tblbookscateg
    fields = ['cdescr']
    labels = {'cdescr': 'Description'}
    widgets = {'cdescr': forms.Textarea(attrs={'rows':1, 'cols':40}),}

class SiteForm(forms.ModelForm):
  class Meta:
    model = Tblbksites
    fields = ['sdescr']
    labels = {'sdescr': 'Description'}
    widgets = {'sdescr': forms.Textarea(attrs={'rows':1, 'cols':40}),}

class LocForm(forms.ModelForm):
  class Meta:
    model = Tblbookslocations
    fields = ['ldescr','site']
    labels = {'ldescr': 'Description'}
    widgets = {
      'ldescr': forms.Textarea(attrs={'rows':1, 'cols':80}),
    }

class LocFromSiteForm(forms.ModelForm):
  class Meta:
    model = Tblbookslocations
    fields = ['ldescr']
    labels = {'ldescr': 'Description'}
    widgets = {
      'ldescr': forms.Textarea(attrs={'rows':1, 'cols':40}),
    }

class BookFromLocForm(forms.ModelForm):
  class Meta:
    model = Tblbook
    fields = ['title','title_en','author','translator','publisher','category']
    widgets = {
      'title': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'title_en': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'author': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'translator': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'publisher': forms.Textarea(attrs={'rows':1, 'cols':80}),
    }

class BookFromCatForm(forms.ModelForm):
  class Meta:
    model = Tblbook
    fields = ['title','title_en','author','translator','publisher','location']
    widgets = {
      'title': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'title_en': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'author': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'translator': forms.Textarea(attrs={'rows':1, 'cols':80}),
      'publisher': forms.Textarea(attrs={'rows':1, 'cols':80}),
    }

class BookForm(forms.ModelForm):
  class Meta:
    model = Tblbook
    fields = ['title','title_en','author','translator','publisher','location','category']
    widgets = {
      'title': forms.Textarea(attrs={'rows':1, 'cols':40}),
      'title_en': forms.Textarea(attrs={'rows':1, 'cols':40}),
      'author': forms.Textarea(attrs={'rows':1, 'cols':40}),
      'translator': forms.Textarea(attrs={'rows':1, 'cols':40}),
      'publisher': forms.Textarea(attrs={'rows':1, 'cols':40}),
    }
