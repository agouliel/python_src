from django.contrib import admin

from .models import Tblbook, Tblbookscateg, Tblbookslocations

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publisher')
  list_filter = ['category', 'location']
  search_fields = ['title']

admin.site.register(Tblbook, BookAdmin)