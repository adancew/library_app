from django import forms
from django.db import models
from shared.models import Book, Comic

AVAILABILITY_CHOICES = (
    ("AVAILABLE", "available"),
    ("DAMAGED", "damaged"),
    ("LOST", "lost"),
    ("BORROWED", "borrowed"),
    ("UNAVAILABLE", "unavailable"),
)

BORROWING_STATUS_CHOICES = (
    ("UNDERWAY", "underway"),
    ("OVERKEPT", "overkept"),
    ("RETURNED", "returned"),
    ("LOST", "lost"),
)

SECTION_CHOICES = (
    ("CHILDREN", "children"),
    ("ADULT", "adult"),

)


class EnterAudiobookForm(forms.Form):
    # resource fields
    title = forms.CharField(label='title')
    status =forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    date_published = forms.DateField(label='date published (format: yyyy-mm-dd)', input_formats=['%Y-%m-%d'])
    section =forms.ChoiceField(choices=SECTION_CHOICES)
    language = forms.CharField(label='language')
    publisher = forms.CharField(label='publisher')
    genre = forms.CharField(label='genre')
    # book-specific fields  
    udc = forms.CharField(label='udc')
    author = forms.CharField(label='author')
    narrator = forms.CharField(label='narrator')


class EnterBookForm(forms.Form):
    # resource fields
    title = forms.CharField(label='title')
    status =forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    date_published = forms.DateField(label='date published (format: yyyy-mm-dd)', input_formats=['%Y-%m-%d'])
    section =forms.ChoiceField(choices=SECTION_CHOICES)
    language = forms.CharField(label='language')
    publisher = forms.CharField(label='publisher')
    genre = forms.CharField(label='genre')
    # specific fields  
    udc = forms.CharField(label='udc')
    isbn = forms.CharField(label='isbn')
    author = forms.CharField(label='author')
    

class EnterComicForm(forms.Form):
    # resource fields
    title = forms.CharField(label='title')
    status =forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    date_published = forms.DateField(label='date published (format: yyyy-mm-dd)', input_formats=['%Y-%m-%d'])
    section =forms.ChoiceField(choices=SECTION_CHOICES)
    language = forms.CharField(label='language')
    publisher = forms.CharField(label='publisher')
    genre = forms.CharField(label='genre')
    # specific fields  
    udc = forms.CharField(label='udc')
    isbn = forms.CharField(label='isbn')
    author = forms.CharField(label='author')
    illustrator = forms.CharField(label='illustrator')

class EnterJournalForm(forms.Form):
    # resource fields
    title = forms.CharField(label='title')
    status =forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    date_published = forms.DateField(label='date published (format: yyyy-mm-dd)', input_formats=['%Y-%m-%d'])
    section =forms.ChoiceField(choices=SECTION_CHOICES)
    language = forms.CharField(label='language')
    publisher = forms.CharField(label='publisher')
    genre = forms.CharField(label='genre')
    # specific fields  
    issn = forms.CharField(label='issn')
    issue = forms.CharField(label='issue')
    
class EnterMovieForm(forms.Form):
    # resource fields
    title = forms.CharField(label='title')
    status =forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    date_published = forms.DateField(label='date published (format: yyyy-mm-dd)', input_formats=['%Y-%m-%d'])
    section =forms.ChoiceField(choices=SECTION_CHOICES)
    language = forms.CharField(label='language')
    publisher = forms.CharField(label='publisher')
    genre = forms.CharField(label='genre')
    # specific fields  
    udc = forms.CharField(label='udc')
    director = forms.CharField(label='director')
    screenwriter = forms.CharField(label='screenwriter')
    producer = forms.CharField(label='producer')
    duration = forms.CharField(label='duration')