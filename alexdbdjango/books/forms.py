from django import forms
from .models import Tblbookscateg, Tblbookslocations, Tblbook

class CategForm(forms.ModelForm):
  class Meta:
    model = Tblbookscateg
    fields = ['cdescr']
    labels = {'cdescr': 'Description'}

class LocForm(forms.ModelForm):
  class Meta:
    model = Tblbookslocations
    fields = ['ldescr']
    labels = {'ldescr': 'Description'}

class BookForm(forms.ModelForm):
  class Meta:
    model = Tblbook
    fields = ['title','title_en','author','translator','publisher']
    widgets = {'title': forms.Textarea(attrs={'rows':2, 'cols':80})}