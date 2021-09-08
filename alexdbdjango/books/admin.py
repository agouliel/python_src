from django.contrib import admin

from .models import Tblbook, Tblbookscateg, Tblbookslocations

class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'translator', 'publisher', 'location')
  list_filter = ['category']
  search_fields = ['title', 'author']

admin.site.register(Tblbook, BookAdmin)
admin.site.register(Tblbookscateg)
admin.site.register(Tblbookslocations)