from django.contrib import admin
from django.forms import Textarea #TextInput
from django.db import models
from django.http import HttpResponse

from .models import Tblfiles

class FileAdmin(admin.ModelAdmin):
  list_display = ('fname',)# 'fcontents')
  search_fields = ['fname']
  actions = ["download_file",]
  formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

  # the below was used for a BLOB field in the db.
  # it worked, but couldn't figure out the upload part,
  # so it was replaced by FileField in models and MEDIA_ROOT in settings
  #def download_file(self, request, queryset):
    #contents = bytes(queryset[0].fcontents)
    #response = HttpResponse(contents)
    #response['ContentDisposition']='attachment;filename=myfile'
    #return response

admin.site.register(Tblfiles, FileAdmin)
