from shared.models import Resource, Journal, Comic, Book, Audiobook, Movie
from .forms import EnterBookForm
import datetime

def get_resources_with_details():
    
    audiobooks = [{
            "id": book.resource_id,
            "type": "audiobook",
            "title": book.resource.title,
            'author': book.author,
            'status': book.resource.status} 
            for book in Audiobook.objects.select_related('resource').all()]

    books = [{
            "id": book.resource_id,
            "type": "książka",
            "title": book.resource.title,
            'author': book.author,
            'status': book.resource.status} 
            for book in Book.objects.select_related('resource').all()]
    
    comics = [{
           "id": comic.resource_id,
            "type": "komiks",
            "title": comic.resource.title,
            'author': comic.author,
            'status': comic.resource.status} 
            for comic in Comic.objects.select_related('resource').all()]
    
    journal = [{
           "id": journal.resource_id,
            "type": "czasopismo",
            "title": journal.resource.title,
            'author': "-",
            'status': journal.resource.status} 
            for journal in Journal.objects.select_related('resource').all()]

    movies = [{
           "id": movie.resource_id,
            "type": "film",
            "title": movie.resource.title,
            'author': "-",
            'status': movie.resource.status} 
            for movie in Movie.objects.select_related('resource').all()]

    return audiobooks + books + comics + journal + movies

def get_resource_category(resource_id:int):
    if Audiobook.objects.filter(resource_id = resource_id).exists():
        return "audiobook"
    if Book.objects.filter(resource_id = resource_id).exists():
        return "book"
    if Comic.objects.filter(resource_id = resource_id).exists():
        return "comic"
    if Journal.objects.filter(resource_id = resource_id).exists():
       return "journal"
    if Movie.objects.filter(resource_id = resource_id).exists():
        return "movie"
    return ""


def get_resource_with_details(resource_id:int):
    res_raw = Resource.objects.get(id=resource_id)
    res_dict = {
        'id': res_raw.id,
        'title': res_raw.title,
        'status': res_raw.status,
        'date_published': res_raw.date_published,
        'section': res_raw.section,
        'language': res_raw.language,
        'publisher': res_raw.publisher,
        'genre': res_raw.genre,
    }

    if Audiobook.objects.filter(resource_id = resource_id).exists():
        r = Audiobook.objects.get(resource_id = resource_id)
        res_dict['category']="audiobook"
        res_dict['udc']=r.udc
        res_dict['author']=r.author
        res_dict['narrator']=r.narrator
        res_dict['book']= r.book_id
        return res_dict
    
    if Book.objects.filter(resource_id = resource_id).exists():
        res_dict['category']="book"
        r = Book.objects.get(resource_id = resource_id)
        res_dict['udc']=r.udc
        res_dict['isbn']=r.isbn
        res_dict['author']=r.author
        return res_dict
    
    if Comic.objects.filter(resource_id = resource_id).exists():
        r = Comic.objects.get(resource_id = resource_id)
        res_dict['category']="comic"
        res_dict['udc']=r.udc
        res_dict['isbn']=r.isbn
        res_dict['author']=r.author
        res_dict['illustrator']=r.illustrator
        return res_dict
    
    if Journal.objects.filter(resource_id = resource_id).exists():
        r = Journal.objects.get(resource_id = resource_id)
        res_dict['category']="journal"
        res_dict['issn']=r.issn
        res_dict['issue']=r.issue
        return res_dict
    
    if Movie.objects.filter(resource_id = resource_id).exists():
        r = Movie.objects.get(resource_id = resource_id)
        res_dict['category']="movie"
        res_dict['udc']=r.udc
        res_dict['director']=r.director
        res_dict['screenwriter']=r.screenwriter
        res_dict['producer']=r.producer
        res_dict['duration']=r.duration
        return res_dict
    
    return res_dict

    

def filter_resources_with_details(search_word:str):
    return list(filter(lambda resource: search_word.lower() in resource['title'].lower(), 
                       get_resources_with_details()))

    
def get_resource_from_form(form):
    title = form.cleaned_data['title']
    status = form.cleaned_data['status'].upper()
    date_published = form.cleaned_data['date_published']
    section = form.cleaned_data['section']
    language = form.cleaned_data['language']
    publisher = form.cleaned_data['publisher']
    genre = form.cleaned_data['genre']
    return Resource(title=title, 
                       status=status, 
                       date_published=date_published, 
                       section=section, 
                       language=language, 
                       publisher=publisher, 
                       genre=genre)

def save_book(form, new_res):
    udc = form.cleaned_data['udc']
    isbn = form.cleaned_data['isbn']
    author = form.cleaned_data['author']
    new_book = Book(udc=udc, isbn=isbn, author=author, resource_id=new_res.id)
    new_book.save()

def save_audiobook(form, new_res):
    udc = form.cleaned_data['udc']
    narrator = form.cleaned_data['narrator']
    author = form.cleaned_data['author']
    new_book = Audiobook(udc=udc, narrator=narrator, author=author, resource_id=new_res.id)
    new_book.save()

def save_comic(form, new_res):
    udc = form.cleaned_data['udc']
    isbn = form.cleaned_data['isbn']
    author = form.cleaned_data['author']
    illustrator = form.cleaned_data['illustrator']
    new_book = Comic(udc=udc, isbn=isbn, author=author, 
                     illustrator=illustrator, resource_id=new_res.id)
    new_book.save()

def save_journal(form, new_res):
    issn = form.cleaned_data['issn']
    issue = form.cleaned_data['issue']
    new_book = Journal(issn=issn, issue=issue, resource_id=new_res.id)
    new_book.save()

def save_movie(form, new_res):
    udc = form.cleaned_data['udc']
    director = form.cleaned_data['director']
    screenwriter = form.cleaned_data['screenwriter']
    producer = form.cleaned_data['producer']
    duration = form.cleaned_data['duration']
    new_book = Movie(udc=udc, director=director, screenwriter=screenwriter, 
                     producer=producer, duration=duration, resource_id=new_res.id)
    new_book.save()

    
def update_resource(old_resource:Resource, new_resource:Resource):
    old_resource.title=new_resource.title
    old_resource.status=new_resource.status
    old_resource.date_published=new_resource.date_published
    old_resource.section=new_resource.section
    old_resource.language=new_resource.language
    old_resource.publisher=new_resource.publisher
    old_resource.genre=new_resource.genre
    
    old_resource.save()


def update_audiobook(form, resource_id):
    res = Audiobook.objects.get(resource_id=resource_id)
    res.udc = form.cleaned_data['udc']
    res.narrator = form.cleaned_data['narrator']
    res.author = form.cleaned_data['author']
    res.save()

def update_book(form,resource_id):
    res = Book.objects.get(resource_id=resource_id)
    res.udc = form.cleaned_data['udc']
    res.isbn = form.cleaned_data['isbn']
    res.author = form.cleaned_data['author']
    res.save()

def update_comic(form, resource_id):
    res = Comic.objects.get(resource_id=resource_id)
    res.udc = form.cleaned_data['udc']
    res.isbn = form.cleaned_data['isbn']
    res.author = form.cleaned_data['author']
    res.illustrator = form.cleaned_data['illustrator']
    res.save()

def update_journal(form, resource_id):
    res = Journal.objects.get(resource_id=resource_id)
    res.issn = form.cleaned_data['issn']
    res.issue = form.cleaned_data['issue']
    res.save()

def update_movie(form, resource_id):
    res = Movie.objects.get(resource_id=resource_id)
    res.udc = form.cleaned_data['udc']
    res.director = form.cleaned_data['director']
    res.screenwriter = form.cleaned_data['screenwriter']
    res.producer = form.cleaned_data['producer']
    res.duration = form.cleaned_data['duration']
    res.save()