from django.db import models
from django.contrib.auth.models import User

class Tblbookscateg(models.Model):
    cid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    cdescr = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'tblbkcat'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.cdescr

class Tblbksites(models.Model):
    sid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    sdescr = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'tblbksites'
        verbose_name = 'Site'

    def __str__(self):
        return self.sdescr

class Tblbookslocations(models.Model):
    lid = models.AutoField(primary_key=True) # this was wrong using inspectdb
    ldescr = models.TextField(blank=True, null=True)
    site = models.ForeignKey(Tblbksites, on_delete=models.CASCADE, db_column='siteid')

    class Meta:
        #managed = False
        db_table = 'tblbkloc'
        verbose_name = 'Location'

    def __str__(self):
        return self.ldescr

    def get_site(self):
        return self.site.sdescr

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner')

    #link = "Edit"

    class Meta:
        #managed = False
        db_table = 'tblbk'
        verbose_name = 'Book'

    def __str__(self):
        return self.title

    def get_site(self):
        return self.location.get_site()
