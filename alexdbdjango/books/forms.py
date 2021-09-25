from django import forms
from .models import Tblbookscateg

class CategForm(forms.ModelForm):
  class Meta:
    model = Tblbookscateg
    fields = ['cdescr']
    labels = {'cdescr': 'Description'}
