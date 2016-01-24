from django.contrib import admin
from .models import ChatLine,TextMessage

# Register your models here.
class ChatLineAdmin(admin.ModelAdmin):
    list_display = ["id","user_one","user_two"]
    model = ChatLine
    
admin.site.register(ChatLine, ChatLineAdmin)

class TextMessageAdmin(admin.ModelAdmin):
    list_display = ["id","text","timestamp","read","send"]
    model = TextMessage
    
admin.site.register(TextMessage, TextMessageAdmin)