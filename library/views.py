from decimal import *
from django.shortcuts import render
from booksdb.models import Books,UserBooks,Genres,BooksGenres,BookFeedbackComments,BookFeedbackRate
from home.models import CustomUser, FollowUser
from myhome.forms import BookListForm
from .forms import UserBookForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from myhome.models import Notify
from search.forms import SearchByForm
import json
from django.db.models import F

# Create your views here.
def getBooks(booksOfUser):
    genresOfAllBooks = {}
    all_entries = UserBooks.objects.all().filter(user = booksOfUser) 
    for obj in all_entries:
        genresOfBook = obj.book.booksgenres_set.all()
        genresOfAllBooks[obj.book.title] = genresOfBook 
    return all_entries,genresOfAllBooks

def addUserBook(owner,book,health,moe,ebook):
    try:
        books = UserBooks.objects.all().filter(user=owner,book=book)
    except ObjectDoesNotExist:
        quan_no = 0
    else:
        quan_no = books.count()
    userbook = UserBooks.objects.create(user = owner,book = book,quantity_no = (quan_no+1),health = health,moe = moe)
    userbook.ebook = ebook
    userbook.save()

def editUserBook(owner,book,quan_no,health,moe,ebook):
    book = UserBooks.objects.get(user=owner,book=book,quantity_no=quan_no)
    book.health = health
    book.moe = moe
    book.ebook = ebook
    book.save()
    
def changeAvailable(request,userBookId):
    userBook = UserBooks.objects.get(id = userBookId)
    if userBook.avail:
        userBook.avail = False
    else:
        userBook.avail = True
    userBook.save()
    return HttpResponseRedirect(reverse('library.views.mylib'))

def deleteUserBook(request,userBookId):
    userBook = UserBooks.objects.get(id = userBookId)
    userBook.delete()
    return HttpResponseRedirect(reverse('library.views.mylib'))
    
def sendRequest(request,email,userBookId):
    other_user = CustomUser.objects.get(email = email)
    userBook = UserBooks.objects.get(id = userBookId)    
    Notify.objects.create(user_sender=request.user,user_reciever=other_user,book_concerned=userBook)
    return HttpResponseRedirect(reverse('library.views.seelibrary',kwargs={'email' : email}))

def seelibrary(request,email):
    if request.user.email == email:
        return HttpResponseRedirect(reverse('library.views.mylib'))
    user_other = CustomUser.objects.get(email = email)
    books,genresOfAllBooks = getBooks(user_other)
    try:
        followUser = FollowUser.objects.get(user_followed = user_other, user_follower = request.user)
    except ObjectDoesNotExist:
        following = False
    else:
        following = True
    context = {
        'other_user' : user_other,
        'books' : books,
        'genresOfAllBooks' : genresOfAllBooks,
        'following' : following
    }
    return render(request,'seelibrary.html',context)

def mylib(request):
    books,genresOfAllBooks = getBooks(request.user)
    errorOutput = ''
    formsInvalid = False
    form1 = BookListForm(request.POST)
    form2 = UserBookForm(request.POST,request.FILES)
    if request.POST:
        if form1.is_valid() and form2.is_valid():
            try:
                book = Books.objects.get(title__iexact = form1.cleaned_data['book'], 
                    author__iexact = form1.cleaned_data['author']
                )
            except ObjectDoesNotExist:
                errorOutput = 'Book Doesn\'t Exist'
            else:
                health = form2.cleaned_data['health']
                moe = form2.cleaned_data['moe']
                ebook = form2.cleaned_data['ebook']
                print ebook
                try:
                    if request.POST['index'] == '':
                        raise KeyError
                except KeyError:
                    addUserBook(request.user,book,health,moe,ebook)
                else:
                    quan_no = request.POST['index']
                    editUserBook(request.user,book,quan_no,health,moe,ebook)
                return HttpResponseRedirect('')
        else:
            formsInvalid = True
    else:
        form1 = BookListForm()
        form2 = UserBookForm()    
    context = {
        'books' : books,
        'form1' : form1,
        'form2' : form2,
        'formsInvalid' : formsInvalid,
        'errorOutput' : errorOutput,
        'genresOfAllBooks' : genresOfAllBooks
    }
    return render(request,'mylib.html',context)

def optionSearch(request,text,option):
    if option == 'title':
        return Books.objects.all().filter(title__iexact = text)
    else:
        return Books.objects.all().filter(author__iexact = text)

def genreSearch(request,text):
    concernedGenre = Genres.objects.get(genre_name__iexact = text)
    bookGenres = BooksGenres.objects.all().filter(genre = concernedGenre)
    books = []
    for bookGenre in bookGenres:
        books.append(bookGenre.book)
    return books
    
def checkSearchByForm(request,form):
    if form.is_valid():
        option = form.cleaned_data['searchOption']
        text = form.cleaned_data['searchBar']
        if text != '':
            if option == 'title' or option == 'author':
                return { 'books' : optionSearch(request,text,option) }
            elif option == 'genre':
                return { 'books' : genreSearch(request,text)}
    else:
        return {}
                    
def theLibrary(request):
    form = SearchByForm(request.GET or None)
    context = {
        'form' : form
    }
    context.update(checkSearchByForm(request,form))
    return render(request,'thelibrary.html',context)
    
def displayBook(request,bookId):
    book = Books.objects.get(isbn = bookId)
    commentHistory = BookFeedbackComments.objects.all().filter(book = book).order_by('timestamp')
    try:
        rating = BookFeedbackRate.objects.get(book = book, user = request.user).rating
    except ObjectDoesNotExist:
        rating = 0
    context = {
        'book' : book,
        'commentHistory' : commentHistory,
        'rating' : rating
    }
    return render(request,'displaybook.html',context)
    
def comments(request,bookId):
    book = Books.objects.get(isbn = bookId)
    comment = request.GET['text']
    newComment = BookFeedbackComments.objects.create(user = request.user,book = book,comment = comment)
    timeStamp = newComment.timestamp.strftime("%d-%m-%Y %H:%M")
    result = [newComment.user.email, timeStamp, newComment.comment]
    return HttpResponse(json.dumps(result), content_type='application/json')
    
def rating(request,bookId):
    book = Books.objects.get(isbn = bookId)
    rating = request.GET['rating']
    try:
        userRating = BookFeedbackRate.objects.get(user = request.user,book = book)
    except ObjectDoesNotExist:
        userRating = BookFeedbackRate.objects.create(user = request.user,book = book,rating = rating)
        book.update(total_rating = F('total_rating') + rating, times_rated = F('times_rated') + 1)
    else:
        book.update(total_rating = F('total_rating') + rating - userRating.rating)
        userRating.rating = rating
        userRating.save()
    finally:
        book.avg_rating = Decimal(book.total_rating)/Decimal(book.times_rated)
        
    return HttpResponse(json.dumps(book.avg_rating), content_type='application/json')