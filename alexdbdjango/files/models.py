from django.db import models

class Tblfiles(models.Model):
    fid = models.AutoField(primary_key=True)
    fname = models.TextField(blank=True, null=True)
    fcontents = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblfiles'
        verbose_name = 'File'

    def __str__(self):
        return self.fname