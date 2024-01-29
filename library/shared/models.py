from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

from decimal import Decimal


class Account(AbstractUser):
    first_name = models.CharField()
    last_name = models.CharField()
    username = models.CharField(unique=True)
    address = models.CharField()
    phone_number = models.CharField()
    email = models.CharField()
    #password=models.CharField(default="")

    USERNAME_FIELD = "username"

    class Meta:
        #managed = False
        db_table = 'account'


class Administrator(models.Model):
    account = models.OneToOneField(Account, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'administrator'


class Card(models.Model):
    type = models.TextField()  # This field type is a guess.
    reader = models.OneToOneField('Reader', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'card'


class Employee(models.Model):
    account = models.OneToOneField(Account, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'employee'


class Reader(models.Model):
    account = models.OneToOneField(Account, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'reader'


class Audiobook(models.Model):
    udc = models.CharField()
    author = models.CharField()
    narrator = models.CharField()
    book = models.ForeignKey('Book', models.DO_NOTHING, blank=True, null=True)
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'audiobook'


class Book(models.Model):
    udc = models.CharField()
    isbn = models.CharField()
    author = models.CharField()
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'book'


class Borrowing(models.Model):
    status = models.TextField()  # This field type is a guess.
    date_borrowed = models.DateField()
    date_due = models.DateField()
    date_returned = models.DateField(blank=True, null=True)
    times_renewed = models.IntegerField()
    reader = models.ForeignKey('Reader', models.DO_NOTHING)
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'borrowing'


class Branch(models.Model):
    name = models.CharField()
    address = models.CharField()

    class Meta:
        #managed = False
        db_table = 'branch'


class Catalogue(models.Model):
    resource = models.ForeignKey('Resource', models.DO_NOTHING)
    branch = models.ForeignKey(Branch, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'catalogue'


class Comic(models.Model):
    udc = models.CharField()
    isbn = models.CharField()
    author = models.CharField()
    illustrator = models.CharField()
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'comic'


class Fee(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(Decimal('0.01'))])
    reason = models.CharField()
    date_issued = models.DateField()
    is_paid = models.BooleanField()
    date_paid = models.DateField(blank=True, null=True)
    reader = models.ForeignKey('Reader', models.DO_NOTHING)
    borrowing = models.ForeignKey(Borrowing, models.DO_NOTHING, blank=True, null=True)
    resource = models.ForeignKey('Resource', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'fee'


class Journal(models.Model):
    issn = models.CharField()
    issue = models.CharField()
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'journal'


class Movie(models.Model):
    udc = models.CharField()
    director = models.CharField()
    screenwriter = models.CharField()
    producer = models.CharField()
    duration = models.CharField()
    resource = models.ForeignKey('Resource', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'movie'


class Resource(models.Model):
    title = models.CharField()
    status = models.TextField()  # This field type is a guess.
    date_published = models.DateField()
    section = models.TextField()  # This field type is a guess.
    language = models.CharField()
    publisher = models.CharField()
    genre = models.CharField()

    class Meta:
        #managed = False
        db_table = 'resource'