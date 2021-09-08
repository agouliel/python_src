from django.contrib import admin
from django.forms import Textarea #TextInput
from django.db import models

from .models import Tblbook, Tblbookscateg, Tblbookslocations

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'translator', 'publisher', 'location')
  list_filter = ['category']
  search_fields = ['title', 'author']
  formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

class CategAdmin(admin.ModelAdmin):
  formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

class LocationAdmin(admin.ModelAdmin):
  formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

admin.site.register(Tblbook, BookAdmin)
admin.site.register(Tblbookscateg, CategAdmin)
admin.site.register(Tblbookslocations, LocationAdmin)