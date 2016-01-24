from django.db import models
from django.conf import settings

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    house_number = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=6)
    lat = models.DecimalField(decimal_places=7,max_digits=10,default=0)
    lon = models.DecimalField(decimal_places=7,max_digits=10,default=0)
    primary = models.BooleanField(default = False)
    
    class Meta:
        unique_together = (('user','house_number','area','city','state','zip_code'),)
        
class BookList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey('booksdb.Books')
    read = models.BooleanField(default = False)
    date_added = models.DateTimeField(blank=True,null=True)
    date_read = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        unique_together = (('user','book'),)
        
class Notify(models.Model):
    user_sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sender')
    user_reciever = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reciever')
    book_concerned = models.ForeignKey('booksdb.UserBooks',null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default = False)
    send = models.BooleanField(default = False)
    class Meta:
        unique_together = (('user_sender','user_reciever','timestamp'),)