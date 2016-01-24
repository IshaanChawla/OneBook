from django.db import models
from django.conf import settings
# Create your models here.

class Books(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    pub_status = models.CharField(max_length=10,default='Yes')
    avg_rating = models.DecimalField(decimal_places=2,max_digits=3,default=0)
    goodread_avg_rating = models.DecimalField(decimal_places=2,max_digits=3,default=0)
    language = models.CharField(max_length=15,default='English')
    description = models.TextField(default='No Description Available')
    book_pic = models.ImageField(upload_to='book_pics/', null=True)
    total_rating = models.IntegerField(default = 0)
    times_rated = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['-goodread_avg_rating']


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.genre_name


class UserInterestedGenres(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    genre = models.ForeignKey('Genres')

    class Meta:
        unique_together = (('user', 'genre'),)


class BooksGenres(models.Model):
    book = models.ForeignKey('Books')
    genre = models.ForeignKey('Genres')

    class Meta:
        unique_together = (('book', 'genre'),)


class UserBooks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey('Books')
    quantity_no = models.IntegerField()
    health = models.DecimalField(decimal_places=2,max_digits=3,default=0)
    avail = models.BooleanField(default=True)
    moe = models.CharField(default='te', max_length=3)
    ebook = models.FileField(upload_to='ebooks/',blank = True,null = True)

    class Meta:
        unique_together = (('user', 'book', 'quantity_no'),)
        
class BookFeedbackComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey('Books')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    comment = models.TextField()
    
    class Meta:
        unique_together = (('user', 'book', 'timestamp'),)
        
class BookFeedbackRate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey('Books')
    rating = models.IntegerField(default=0)
    
    class Meta:
        unique_together = (('user', 'book'),)