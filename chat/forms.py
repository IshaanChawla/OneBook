from booksdb.models import UserBooks
from django import forms
from django.db.models import Q
  
class DownloadLinkForm(forms.Form):
    def __init__(self,requestingUser,*args,**kwargs):
        super(DownloadLinkForm, self).__init__(*args, **kwargs)
    
        all_entries = UserBooks.objects.all().filter(Q(user = requestingUser) & ~Q(ebook = ''))
        book_list = []
        for obj in all_entries:
            tup = (obj.id,obj.book.title)
            book_list.append(tup)
        
        OPTION = tuple(book_list)
            
        self.fields['ebookOption'] = forms.ChoiceField(required = True,
            widget=forms.RadioSelect,
            choices = OPTION,
            label = ''
        )