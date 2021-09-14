from django.contrib import admin
from django.forms import Textarea #TextInput
from django.db import models

from .models import Tblsongs

class SongAdmin(admin.ModelAdmin):
  list_display = ('title', 'artist', 'album', 'composer')
  search_fields = ['title', 'artist', 'album', 'composer']
  formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

admin.site.register(Tblsongs, SongAdmin)
