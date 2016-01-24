from decimal import *
from django.shortcuts import render
from myhome.models import Address,Notify
from booksdb.models import Books, BooksGenres, UserBooks, UserInterestedGenres, Genres
from home.models import CustomUser
from .forms import SearchByForm,RadiusForm,SelectAddressForm
import json
from django.http import HttpResponse
from django.db.models import Q
import operator

# Create your views here.
class LatLon():
    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.email = ''
    def set(self,lat,lon,email):
        self.lat = lat
        self.lon = lon
        self.email = email

def userhasGenre(other,my_fav_genres):
    my_books = UserBooks.objects.all().filter(user = other)
    for mybook in my_books:
        book_genres = BooksGenres.objects.all().filter(book = mybook.book)
        for bg in book_genres:
            if bg.genre in my_fav_genres:
                return True
    return False
    
def genreSearch(request,near_by_add,genre=None):
    my_fav_genres = []
    if genre == None:
        fav_genres = UserInterestedGenres.objects.all().filter(user = request.user)
        for obj in fav_genres:
            my_fav_genres.append(obj.genre)
    else:
        my_fav_genres = Genres.objects.all().filter(genre_name__iexact = genre)
        
    latlon = [LatLon() for i in range(len(near_by_add)-1)]
    j = 0
    for i in range(near_by_add.count()):
        other = CustomUser.objects.get(email = near_by_add[i].user.email)
        if other != request.user and userhasGenre(other,my_fav_genres):
            latlon[j].set(near_by_add[i].lat,near_by_add[i].lon,other.email)
            j += 1
    
    return latlon
    
def userhasBook(other,books):
    my_books = UserBooks.objects.all().filter(user = other)
    for mybook in my_books:
        if mybook.book in books:
            return True
    else:
        return False
        
def optionSearch(request,near_by_add,text,option):
    if option == 'title':
        books = Books.objects.all().filter(title__iexact = text)
    else:
        books = Books.objects.all().filter(author__iexact = text)
        
    latlon = [LatLon() for i in range(len(near_by_add)-1)]
    for i in range(near_by_add.count()):
        other = CustomUser.objects.get(email = near_by_add[i].user.email)
        if other != request.user and userhasBook(other,books):
             latlon[i].set(near_by_add[i].lat,near_by_add[i].lon,other.email)
    return latlon
            
def checkSearchByForm(request,near_by_add,form):
    if form.is_valid():
        option = form.cleaned_data['searchOption']
        text = form.cleaned_data['searchBar']
        if text != '':
            if option == 'title' or option == 'author':
                latlon = optionSearch(request,near_by_add,text,option)
            elif option == 'genre':
                latlon = genreSearch(request,near_by_add,text)
        else:
            latlon = genreSearch(request,near_by_add)
    else:
        latlon = genreSearch(request,near_by_add)
    return latlon
    
def checkRadiusForm(request,form,mylat,mylon):
    if form.is_valid():
        option = form.cleaned_data['radiusOption']
        if option == '5':
            radius = 0.045
        elif option == '10':
            radius = 0.090
        elif option == '15':
            radius = 0.135
    else:
        radius = 0.045
    near_by_add = Address.objects.all().filter(lat__gte=mylat-Decimal(radius),
                                        lat__lte=mylat+Decimal(radius),
                                        lon__gte=mylon-Decimal(radius),
                                        lon__lte=mylon+Decimal(radius)
                                        )
    return near_by_add
    
def checkSelectAddressForm(request,form,defaultAddress,myadd):
    if form.is_valid():
        currentAddress = myadd.get(id = form.cleaned_data['addressOption'])
        mylat = currentAddress.lat
        mylon = currentAddress.lon
    else:
        mylat = defaultAddress.lat
        mylon = defaultAddress.lon
    return mylat,mylon
    
def search(request):
    myadd = request.user.address_set.all()
    defaultAddress = myadd.get(primary = True)
    
    form3 = SelectAddressForm(request.user,
            request.GET or None, 
            initial = {'addressOption' : defaultAddress.id}
        )
    mylat,mylon = checkSelectAddressForm(request,form3,defaultAddress,myadd)

    form2 = RadiusForm(request.GET or None, initial = {'radiusOption' : '5'})
    near_by_add = checkRadiusForm(request,form2,mylat,mylon)
    
    form1 = SearchByForm(request.GET or None)                           
    latlon = checkSearchByForm(request,near_by_add,form1)
    
    context = {
        'mylon' : mylon,
        'mylat' : mylat,
        'latlon' : latlon,
        'form1' : form1,
        'form2' : form2,
        'form3' : form3
    }
    return render(request,'search.html',context)
    
def searchall(request):
    searchTitleQuery = Books.objects.all().filter(title__icontains = request.GET['search'])
    searchAuthorQuery = Books.objects.all().filter(author__icontains = request.GET['search'])
    searchGenreQuery = Genres.objects.all().filter(genre_name__icontains = request.GET['search'])
    results = []
    for result in searchTitleQuery:
        results.append(result.title)
    for result in searchAuthorQuery:
        results.append(result.author)
    for result in searchGenreQuery:
        results.append(result.genre_name)
    return HttpResponse(json.dumps(results[0:5]), content_type='application/json')
    
def seeNotification(request):
    notifications = Notify.objects.all().filter(user_reciever = request.user,send = False)
    results = []
    for notification in notifications:
        sender = notification.user_sender.email
        book = notification.book_concerned.book.title
        notification.send = True
        notification.save()
        results.append(sender + '_has sent you an Exchange Request ' + book)
    return HttpResponse(json.dumps(results), content_type='application/json')