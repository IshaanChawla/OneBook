from booksdb.models import Genres
from django.core.management.base import BaseCommand
from django.db import IntegrityError

class Command(BaseCommand):
    def handle(self,*args,**options):
        genreList = ['Drama', 'Classics', 'Comic', 'Crime', 'Fable', 'Fairy Tales', 'Fantasy', 'Fiction', 'Folklore', 'History','Horror', 'Humor',
                'Historical Fiction', 'Legend', 'Magical Realism', 'Metafiction', 'Mystery','Mythology','Mythopeia', 'Science Fiction', 'Short Stories',
                'Suspense', 'Thriller', 'Tall Tale', 'Western','Biography', 'Essay', 'Narrative Nonfiction', 'Speech', 'Textbook', 'Reference book',
                'Self Help', 'Adult','Childrens', 'Poetry', 'Play', 'Literature', 'Romance','Adventure']
        for genre in genreList:
            try:
                Genres.objects.create(genre_name = genre)
            except IntegrityError:
                pass