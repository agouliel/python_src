from django.db import models

class Tblfiles(models.Model):
    fid = models.AutoField(primary_key=True)
    fname = models.TextField(blank=True, null=True)

    # the below was used for a BLOB field in the db
    # (populated using readfile() in sqlite)
    #fcontents = models.BinaryField(blank=True, null=True)

    # but it was replaced by the below, which uploads files
    # directly in the server's filesystem using MEDIA_ROOT in settings.py
    fcontents = models.FileField()

    class Meta:
        #managed = False
        db_table = 'tblfiles'
        verbose_name = 'File'

    def __str__(self):
        return self.fname

