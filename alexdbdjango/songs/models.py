from django.db import models

class Tblsongs(models.Model):
    sid = models.AutoField(primary_key=True)
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    artist = models.TextField(db_column='Artist', blank=True, null=True)
    composer = models.TextField(db_column='Composer', blank=True, null=True)
    album = models.TextField(db_column='Album', blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'tblsong'
        verbose_name = 'Song'

    def __str__(self):
        return self.title

