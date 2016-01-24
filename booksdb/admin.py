from django.contrib import admin
from .models import Books,Genres,BooksGenres,UserInterestedGenres,UserBooks,BookFeedbackComments,BookFeedbackRate
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ["title","author"]
    model = Books
    
admin.site.register(Books, BooksAdmin)

class GenresAdmin(admin.ModelAdmin):
    list_display = ["genre_name"]
    model = Genres
    
admin.site.register(Genres, GenresAdmin)

class BooksGenresAdmin(admin.ModelAdmin):
    list_display = ["book","genre"]
    model = BooksGenres
    
admin.site.register(BooksGenres, BooksGenresAdmin)

class UserInterestedGenresAdmin(admin.ModelAdmin):
    list_display = ["user","genre"]
    model = UserInterestedGenres
    
admin.site.register(UserInterestedGenres, UserInterestedGenresAdmin)

class UserBooksAdmin(admin.ModelAdmin):
    list_display = ["user","book"]
    model = UserBooks
    
admin.site.register(UserBooks, UserBooksAdmin)

class BookFeedbackCommentsAdmin(admin.ModelAdmin):
    list_display = ["user","book","comment","timestamp"]
    model = BookFeedbackComments
    
admin.site.register(BookFeedbackComments,BookFeedbackCommentsAdmin)


class BookFeedbackRateAdmin(admin.ModelAdmin):
    list_display = ["user","book","rating"]
    model = BookFeedbackRate
    
admin.site.register(BookFeedbackRate,BookFeedbackRateAdmin)