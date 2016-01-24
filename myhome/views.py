from .forms import BasicProfileForm, ProfileForm, AddressForm, InterestForm, BookListForm
from .models import Address, BookList, Notify
from booksdb.models import Genres,UserInterestedGenres,Books ,BooksGenres
from chat.models import TextMessage,ChatLine
from datetime import datetime
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
import urllib,urllib2
import json
import operator
# Create your views here.

def addlatlong(instance):
    address = instance.area + ' ' + instance.city + ' ' + instance.state + ' ' + instance.zip_code
    params = {'address': address, 'sensor' : 'false', 'oe': 'utf8'}
    url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)
    rawreply = urllib2.urlopen(url).read()
    reply = json.loads(rawreply)
    if reply['status'] == 'OK':
        obj = reply['results'][0]
        instance.lat = obj['geometry']['location']['lat']
        instance.lon = obj['geometry']['location']['lng']
        
def deleteanyquery(obj):
    obj.delete()
    
def setPrimary(address):
    address.primary = True
    address.save()
     
def saveBasicProfileForm(request,form):
    instance = request.user
    instance.email = form.cleaned_data['email']
    instance.full_name = form.cleaned_data['full_name']
    instance.save()
    
def saveProfileForm(request,form):
    instance = request.user
    instance.sex = form.cleaned_data['sex']
    instance.phone_no = form.cleaned_data['phone_no']
    instance.profile_pic = form.cleaned_data['profile_pic']
    if instance.profile_pic == None:
        instance.profile_pic = 'profile_pics/default_pic.png'
    instance.profile_status = True
    instance.save()
    
def saveAddressForm(request,form,primary,address):
    if address == None:
        add_instance = form.save(commit=False)
        add_instance.user = request.user
    else:
        add_instance = address
        add_instance.house_number = form.cleaned_data['house_number']
        add_instance.area = form.cleaned_data['area']
        add_instance.city = form.cleaned_data['city']
        add_instance.state = form.cleaned_data['state']
        add_instance.zip_code = form.cleaned_data['zip_code']
    add_instance.primary = primary
    addlatlong(add_instance)
    add_instance.save()
    
def saveInterestForm(request,form,choice):
    for gid in choice:
        genre = Genres.objects.all().filter(genre_id = gid)[0]
        UserInterestedGenres.objects.create(user = request.user,genre = genre,)
    request.user.preference_status = True
    request.user.save()

def profileCheck(request):
    form1 = ProfileForm(request.POST, request.FILES)
    form2 = AddressForm(request.POST)
    if request.POST:
        if form1.is_valid() and form2.is_valid():
            saveProfileForm(request,form1)
            saveAddressForm(request,form2,True,None)
            return {}
    else:
        form1 = ProfileForm()
        form2 = AddressForm()                
        context = {
            'form1' : form1,
            'form2' : form2
        }
    return context

def addmarker(request,add):
    print 'adding the marker'
    lat = add.lat
    lon = add.lon
    
    if request.POST:
        print 'Saving the Form'
        add.lat = request.POST['lat']
        add.lon = request.POST['lon']
        add.save()
        request.user.address_on_map = True
        request.user.save()
        return {}
    
    context = {
        'lat' : lat,
        'lon' : lon
    }
    
    return context

def interestCheck(request):
    form = InterestForm(request.POST or None)
    state = 'Give 5 choices'
    if request.POST:
        choice = request.POST.getlist('interested_genres')
        if len(choice) < 5:
            state = 'You havent given 5 choices'
        else:
            saveInterestForm(request,form,choice)
            return {}
    context = {
        'state' : state,
        'form' : form
    }
    return context
    
def getNotifications(notifiedUser):
    notifications = Notify.objects.all().filter(user_reciever = notifiedUser)
    results = []
    numberOfNotifications = 0
    for notification in notifications:
        if not notification.send:
            sender = notification.user_sender.full_name
            book = notification.book_concerned.book
            if not notification.send:
                notification.send = True
                notification.save()
            results.append({'userBook' : book.title,'sender' : sender})
        numberOfNotifications += 1
        
    return {'notes' : results}

def getOfflineTextMessages(notifiedUser):
    chatLines = ChatLine.objects.all().filter(Q(user_one = notifiedUser) | Q(user_two = notifiedUser))
    chatMessages = []
    messageByNewUser = []
    for chatLine in chatLines:
        textMessages = TextMessage.objects.all().filter(~Q(sender = notifiedUser) & Q(read = False,chat = chatLine)).order_by('-timestamp')
        for textMessage in textMessages:
            textMessage.read = True
            textMessage.save()
            if textMessage.sender not in messageByNewUser: 
                messageByNewUser.append(textMessage.sender)
                chatMessages.append(textMessage)
                
    return {'chatMessages' : chatMessages}
    
def interestedGenres(theUser):
    userGenres = {}
    userInterestedGenres = UserInterestedGenres.objects.all().filter(user = theUser)
    for uig in userInterestedGenres:
        userGenres[uig.genre] = 3 
    return userGenres
    
def readBooksGenres(theUser,userGenres):
    readBooks = BookList.objects.all().filter(user = theUser, read = True)
    readBookGenres = []
    for aReadBook in readBooks:
        readBookGenres.append(BooksGenres.objects.all().filter(book = aReadBook.book))
    for aList in readBookGenres:
        for aBookGenre in aList:
            try:
                userGenres[aBookGenre.genre] += 1
            except KeyError:
                userGenres[aBookGenre.genre] = 1
    return userGenres
    
def wishBooksGenres(theUser,userGenres):
    wishBooks = BookList.objects.all().filter(user = theUser, read = False)
    wishBookGenres = []
    for aReadBook in wishBooks:
        wishBookGenres.append(BooksGenres.objects.all().filter(book = aReadBook.book))
    for aList in wishBookGenres:
        for aBookGenre in aList:
            try:
                userGenres[aBookGenre.genre] += 2
            except KeyError:
                userGenres[aBookGenre.genre] = 2
    return userGenres
    
def getRecommendations(theUser):
    userGenres = interestedGenres(theUser)
    userGenres = readBooksGenres(theUser,userGenres)
    userGenres = wishBooksGenres(theUser,userGenres)
    bookRecommendations = {}
    for key in userGenres:
        booksOfaGenre = BooksGenres.objects.all().filter(genre = key).order_by('book')
        bookRecommendations[key] = booksOfaGenre[0:4]
    return {'bookRecommendations' : bookRecommendations}
        
def userhome(request):
    if request.user.is_authenticated():
        context = {}
        while context == {}:
            if not request.user.profile_status:
                context = profileCheck(request)
            elif not request.user.address_on_map:
                add = Address.objects.all().filter(user = request.user)[0]
                context = addmarker(request,add)
            elif not request.user.preference_status:
                context = interestCheck(request)
            else:
                context.update(getOfflineTextMessages(request.user))
                context.update(getNotifications(request.user))
                context.update(getRecommendations(request.user))
            request.POST = None
        return render(request,'userhome.html',context)
    else:
        return HttpResponseRedirect(reverse('home.views.signin'))
   
def profileEdit(request):
    form1 = BasicProfileForm(request.POST)
    form2 = ProfileForm(request.POST, request.FILES)
    if request.POST:
        if form1.is_valid() and form2.is_valid():
            saveBasicProfileForm(request,form1)
            saveProfileForm(request,form2)
    else:
        form1 = BasicProfileForm(initial = {'email' : request.user.email,
                    'full_name' : request.user.full_name
                }
            )
        form2 = ProfileForm(initial = {'sex' : request.user.sex,
                    'phone_no' : request.user.phone_no,
                    'profile_pic' : request.user.profile_pic
                }
            )
    context = {
        'form1' : form1,
        'form2' : form2
    }
    return render(request,'editprofile.html',context)
    
def primaryAddress(request,addressId):
    addresses = Address.objects.all().filter(user = request.user)
    address = addresses.get(primary = True)
    address.primary = False
    address.save()
    setPrimary(addresses.get(id = addressId))
    return HttpResponseRedirect(reverse('myhome.views.addressEdit'))

def deleteAddress(request,addressId):
    addresses = Address.objects.all().filter(user = request.user)
    address = addresses.get(id = addressId)
    if address.primary == True:
        setPrimary(addresses[0])
    deleteanyquery(address)
    return HttpResponseRedirect(reverse('myhome.views.addressEdit'))
    
def addressEdit(request):
    index = None
    addresses = Address.objects.all().filter(user = request.user)
    checkForm = True    
    if request.POST:           
        try:
            if request.POST['mark'] == '':
                raise KeyError
        except KeyError:
            print 'Bye'
            pass
        else:
            print 'done checking'
            address = addresses.get(id = request.POST['mark'])
            context = addmarker(request,address)
            checkForm = False
            
        if checkForm:
            form = AddressForm(request.POST or None)
            if form.is_valid():
                index = request.POST['index']
                if  index != '-1':
                    address = addresses.get(id = index)
                    primary = address.primary
                else:
                    address = None
                    primary = False
                saveAddressForm(request,form,primary,address)
                if address == None:
                    address = addresses[len(addresses)-1]
                    index = address.id
        else:
            form = AddressForm()
    else:
        form = AddressForm()
    
    canDelete = False
    if len(addresses) > 1:
        canDelete = True

    context = {
        'addresses' : addresses,
        'form' : form,
        'index' : index,
        'canDelete' : canDelete
    }
    if index != None:
        request.POST = None
        context.update(addmarker(request,address))
    
    return render(request,'editaddress.html',context)
    
def preferenceEdit(request):
    form = InterestForm(request.POST or None)
    preferedGenres = UserInterestedGenres.objects.all().filter(user = request.user)
    state = 'Atleast 5 Choices' 
    if request.POST:
        deleteanyquery(preferedGenres)
        choice = request.POST.getlist('interested_genres')
        if len(choice) < 5:
            state = 'You havent given 5 choices'
        else:
            saveInterestForm(request,form,choice)
    else:
        savedList = []
        for aGenre in preferedGenres:
            savedList.append(aGenre.genre.genre_id)
        form = InterestForm(initial={'interested_genres' : savedList})
    context = {
        'form' : form,
        'state' : state
    }
    return render(request,'editpreference.html',context)
    
def deleteListBook(request,bookListId,url):
    deleteanyquery(BookList.objects.get(id = bookListId))
    return HttpResponseRedirect(url)

def readListBook(request,bookListId):
    book = BookList.objects.get(id = bookListId)
    book.read = True
    book.date_read = datetime.now()
    book.save()
    return HttpResponseRedirect(reverse('myhome.views.sharefb',kwargs={'bookListId' : book.id, 'email' : request.user.email}))

def wishlist(request):
    errorOutput = ''
    wishListBooks = BookList.objects.all().filter(user = request.user,read = False)
    form = BookListForm(request.POST or None)
    if form.is_valid():
        try:
            book = Books.objects.get(title__iexact = form.cleaned_data['book'], 
                author__iexact = form.cleaned_data['author']
            )
        except ObjectDoesNotExist:
            errorOutput = 'Book Doesn\'t Exist'
        else:
            BookList.objects.create(user = request.user, book = book, date_added = datetime.now())
            return HttpResponseRedirect('')
            
    context = {
        'form1' : form,
        'errorOutput' : errorOutput,
        'wishListBooks' : wishListBooks
    }
    return render(request,'wishlist.html',context)

def readlist(request):
    errorOutput = ''
    readListBooks = BookList.objects.all().filter(user = request.user,read = True)
    form = BookListForm(request.POST or None)
    if form.is_valid():
        try:
            book = Books.objects.get(title__iexact = form.cleaned_data['book'], 
                author__iexact = form.cleaned_data['author']
            )
        except ObjectDoesNotExist:
            errorOutput = 'Book Doesn\'t Exist'
        else:
            book = BookList.objects.create(user = request.user, book = book, read = True, date_read = datetime.now())
            return HttpResponseRedirect(reverse('myhome.views.sharefb',kwargs={'bookListId' : book.id, 'email' : request.user.email}))
    context = {
        'form1' : form,
        'errorOutput' : errorOutput,
        'readListBooks' : readListBooks
    }
    return render(request,'readlist.html',context)

def sharefb(request,bookListId,email):
    book = BookList.objects.get(id = bookListId)
    context= {
        'book' : book
    }
    return render(request,'sharefb.html',context)
            
def loguserout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home.views.signin'))