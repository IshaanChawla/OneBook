from django.db import models
from django.conf import settings

# Create your models here.
class ChatLine(models.Model):
    user_one = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_one')
    user_two = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_two')
    
class TextMessage(models.Model):
    chat = models.ForeignKey('chat.ChatLine')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null = True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.CharField(max_length=500)
    read = models.BooleanField(default = False)
    send = models.BooleanField(default = False)
    
    class Meta:
        unique_together = (('chat', 'timestamp'),)