from django.db import models

class Tblbookscateg(models.Model):
    cid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    cdescr = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblbookscateg'

    def __str__(self):
        return self.cdescr


class Tblbookslocations(models.Model):
    lid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    ldescr = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblbookslocations'

    def __str__(self):
        return self.ldescr

class Tblbook(models.Model):
    bid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    title = models.TextField(blank=True, null=True)
    title_en = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    translator = models.TextField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)

    #locid = models.IntegerField(blank=True, null=True)
    #catid = models.IntegerField(blank=True, null=True)

    location = models.ForeignKey(Tblbookslocations, on_delete=models.CASCADE, db_column='locid')
    category = models.ForeignKey(Tblbookscateg, on_delete=models.CASCADE, db_column='catid')

    class Meta:
        managed = False
        db_table = 'tblbook'

    def __str__(self):
        return self.title
