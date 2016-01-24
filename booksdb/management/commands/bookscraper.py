# Scrapping GoodReads for book names, authors, images, descriptions and ratings

import requests
import os
import urllib
#import threading
from booksdb.models import Books,BooksGenres,Genres
from django.db import IntegrityError
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.core.files import File

genreList = []
def initializer(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup
        
class Threads():
    def __init__(self,link):
        #threading.Thread.__init__(self)
        self.link = link
        
    def run(self):
        allBookLinks = self.getLinks(self.link)
        try:
            for link in allBookLinks:
                self.getContentAndUpload(link)
        except Exception:
            pass    
    def getLinks(self,link):
        soup = initializer(link)
        allLinksInPage = soup.find_all('a')
        allBookLinks = []
        for link in allLinksInPage:
            stringLink = link.get('href')
            try:
                if stringLink is None:
                    raise TypeError
            except TypeError:
                pass
            else:
                BookLink = '/book/show' in stringLink
                try:
                    lastRecievedLink = not (stringLink in allBookLinks[len(allBookLinks) - 1])
                except IndexError:
                    lastRecievedLink = True
                finally:
                    if BookLink and lastRecievedLink:
                        allBookLinks.append('https://www.goodreads.com' + stringLink)
        return allBookLinks
    
    
    def getBookName(self,soup):
        titleDiv = soup.find_all('h1', {'class': 'bookTitle'})[0]
        # Cleaning the Book Title
        textRecieved = " ".join(titleDiv.text.split())
        bookTitle = ''
        index = 0
        while index < len(textRecieved):
            if textRecieved[index] != '(':
                bookTitle += textRecieved[index]
            else:
                break
            index += 1
        bookTitle = " ".join(bookTitle.split())
        return bookTitle
    
    
    def getBookAuthor(self,soup):
        authorDiv = soup.find_all('div', {'id': 'bookAuthors'})[0]
        # Cleaning the Author Name
        textRecieved = " ".join(authorDiv.text.split())
        bookAuthor = ''
        index = 0
        while textRecieved[index] != ' ':
            index += 1
        index += 1
        while index < len(textRecieved):
            if textRecieved[index] != ',' and textRecieved[index] != '(':
                bookAuthor += textRecieved[index]
            else:
                break
            index += 1
        bookAuthor = " ".join(bookAuthor.split())
        return bookAuthor
    
    
    def getBookDescription(self,soup):
        try:
            descriptionDiv = soup.find_all('div', {'id': 'description'})[0]
        except IndexError:
            return 'No Description Available'
        else:
            bookDescription = descriptionDiv.text.split('\n')
            # Cleaning the book description
            try:
                if bookDescription[2] == '':
                    raise ValueError
            except ValueError:
                return bookDescription[1]
            else:
                return bookDescription[2]
    
    
    def getBookRating(self,soup):
        try:
            RatingDiv = soup.find_all('span', {'class': 'value rating'})[0]
        except IndexError:
            return '0.0'
        else:
            return RatingDiv.text
    
    def getBookImage(self,soup,bookTitle):
        try:
            image = soup.find_all('img', {'id': 'coverImage'})[0]
        except IndexError:
            filepath = os.path.join('/home/ishaan/Downloads/book_pics/','default.jpg')
        else:
            img_url = 'http:' + image.get('src').split(':')[1]
            img_ext = (((img_url.split('/'))[-1]).split('.'))[-1]
            filename = bookTitle + '.' + img_ext
            filepath = os.path.join('/home/ishaan/Downloads/book_pics/',filename)
            urllib.urlretrieve(img_url, filepath)
        finally:
            return filepath
    
    def getIsbn(self,soup):
        try:
            isbnDiv = soup.find_all('span', {'itemprop': 'isbn'})[0]
        except IndexError:
            return None
        else:
            return isbnDiv.text
    
    def getLanguage(self,soup):
        try:
            langDiv = soup.find_all('div', {'itemprop': 'inLanguage'})[0]
        except IndexError:
            return 'English'
        else:
            return langDiv.text
    
    
    def getGenres(self,soup):
        linksDiv = soup.find_all('a', {'class': 'actionLinkLite'})
        genreDiv = []
        for link in linksDiv:
            if '/genres' in link.get('href'):
                if link.text in genreList and link.text not in genreDiv:
                    genreDiv.append(link.text)
        return genreDiv
    
    
    def getContentAndUpload(self,link):
        soup = initializer(link)
        try:
            bookIsbn = self.getIsbn(soup)
            bookTitle = self.getBookName(soup)
            bookAuthor = self.getBookAuthor(soup)
        except ValueError:
            return
        else:
            bookImgPath = self.getBookImage(soup, bookTitle)
            bookDescription = self.getBookDescription(soup)
            bookRating = self.getBookRating(soup)
            bookLang = self.getLanguage(soup)
            bookGenres = self.getGenres(soup)
            try:
                book = Books.objects.create(isbn=bookIsbn,title=bookTitle,author=bookAuthor,goodread_avg_rating=bookRating,
                                        language=bookLang,description=bookDescription,)
                book.book_pic.save(bookImgPath[-1], File(open(bookImgPath, 'r')))
            except IntegrityError:
                pass
            else:
                for aGenre in bookGenres:
                    book_genre = Genres.objects.all().filter(genre_name = aGenre)[0]
                    BooksGenres.objects.create(book = book,genre = book_genre)
        
class Command(BaseCommand):
    def handle(self,*args,**options):
        global genreList 
        genreList = ['Drama', 'Classics', 'Comic', 'Crime', 'Fable', 'Fairy Tales', 'Fantasy', 'Fiction', 'Folklore', 'History','Horror', 'Humor',
                'Historical Fiction', 'Legend', 'Magical Realism', 'Metafiction', 'Mystery','Mythology','Mythopeia', 'Science Fiction', 'Short Stories',
                'Suspense', 'Thriller', 'Tall Tale', 'Western','Biography', 'Essay', 'Narrative Nonfiction', 'Speech', 'Textbook', 'Reference book',
                'Self Help', 'Adult','Childrens', 'Poetry', 'Play', 'Literature', 'Romance','Adventure']
                
        start_link = ['http://www.goodreads.com/list/show/1.Best_Books_Ever?page=331']
        #threads = []
        
        while(True):
            try:
                print start_link[-1]
                start_link.append(self.getNextLink(start_link[-1]))
                aThread = Threads(start_link[-1])
                aThread.run()
            except ValueError:
                break
                
        #for link in start_link:
        #    aThread = Threads(link)
        #    threads.append(aThread)
        #
        #for aThread in threads:
        #    aThread.start()
        #    
        #for aThread in threads:
        #    aThread.join()
    
                
    def getNextLink(self,link):
        soup = initializer(link)
        nextPageLink = soup.find_all('a',{'class','next_page'})[0].get('href')
        if 'list/show/' in nextPageLink:
            return 'http://www.goodreads.com' + nextPageLink
        else:
            raise ValueError