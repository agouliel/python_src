from django.contrib import admin
from django.forms import Textarea #TextInput
from django.db import models
from django.http import HttpResponse
from django.conf import settings
import os
from os.path import basename
from zipfile import ZipFile
from .models import Tblfiles

class FileAdmin(admin.ModelAdmin):
  list_display = ('fname',)# 'fcontents')
  search_fields = ['fname']
  actions = ["download_file"]
  formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
  }

  # The below was initially used when the db field was BLOB,
  # and the model field was BinaryField.
  # It worked, but the upload part couldn't be figured out,
  # so the model field was replaced by FileField, plus MEDIA_ROOT in settings.
  # The db field remained BLOB though.

  def download_file(self, request, queryset):
    #contents = bytes(queryset[0].fcontents)
    #response = HttpResponse(contents)
    #response['ContentDisposition'] = 'attachment;filename=myfile'

    if len(queryset) == 1:
      file_path = os.path.join(settings.MEDIA_ROOT, str(queryset[0].fcontents))
      myfile = open(file_path,"rb")
      contents = myfile.read()
      myfile.close()
      response = HttpResponse(contents, headers={
        #'Content-Type': 'application/vnd.ms-excel',
        'Content-Disposition': 'attachment; filename="' + str(queryset[0].fcontents) + '"',
      })
    else:
      zip_file_path = os.path.join(settings.MEDIA_ROOT, 'files.zip')
      zipObj = ZipFile(zip_file_path, 'w')
      for item in queryset:
        file_path = os.path.join(settings.MEDIA_ROOT, str(item.fcontents))
        zipObj.write(file_path, basename(file_path))
      zipObj.close()
      myfile = open(zip_file_path,"rb")
      contents = myfile.read()
      myfile.close()
      os.remove(zip_file_path)
      response = HttpResponse(contents, headers={
        'Content-Disposition': 'attachment; filename="files.zip"',
      })

    return response


  def delete_queryset(self, request, queryset):
    for item in queryset:
      file_path = os.path.join(settings.MEDIA_ROOT, str(item.fcontents))
      os.remove(file_path)
    queryset.delete()

  def delete_model(self, request, obj):
    file_path = os.path.join(settings.MEDIA_ROOT, str(obj.fcontents))
    os.remove(file_path)
    obj.delete()

admin.site.register(Tblfiles, FileAdmin)
