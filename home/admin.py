from django.contrib import admin
from .models import CustomUser,FollowUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email","full_name"]
    model = CustomUser
    
admin.site.register(CustomUser, CustomUserAdmin)

class FollowUserAdmin(admin.ModelAdmin):
    list_display = ["user_followed","user_follower"]
    model = FollowUser
    
admin.site.register(FollowUser, FollowUserAdmin)