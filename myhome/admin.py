from django.contrib import admin
from .models import Address,BookList,Notify

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user","city","zip_code"]
    model = Address
    
admin.site.register(Address, AddressAdmin)

class BookListAdmin(admin.ModelAdmin):
    list_display = ["user","book","read"]
    model = BookList
    
admin.site.register(BookList, BookListAdmin)

class NotifyAdmin(admin.ModelAdmin):
    list_display = ["user_sender","user_reciever","read"]
    model = Notify
    
admin.site.register(Notify, NotifyAdmin)