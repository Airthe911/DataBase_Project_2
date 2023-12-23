from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.CharField(max_length=100, null=True,blank=True)
    title = models.CharField(max_length=100, null=True,blank=False)
    author = models.CharField(max_length=100, null=True,blank=False)
    publisher = models.CharField(max_length=100, null=True,blank=True)
    original_title = models.CharField(max_length=100, null=True,blank=False)
    translator = models.CharField(max_length=100, null=True,blank=False)
    pub_year = models.CharField(max_length=100, null=True,blank=False)
    pages = models.DecimalField(max_digits=10, decimal_places=0, null=True,blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=False)
    currency_unit = models.CharField(max_length=100, null=True,blank=True)
    binding = models.CharField(max_length=100, null=True,blank=True)
    isbn = models.CharField(max_length=100, null=True,blank=True)
    author_intro = models.TextField()
    book_intro = models.TextField()
    tags = models.CharField(max_length=300, null=True,blank=True)

class Store(models.Model):
    store_id = models.CharField(max_length=100, null=True,blank=True)
    book_id = models.CharField(max_length=100, null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=False)
    stock_level = models.DecimalField(max_digits=10, decimal_places=0, null=True,blank=False)

class User(models.Model):
    user_id = models.CharField(max_length=100, null=True,blank=True)
    password = models.CharField(max_length=100, null=True,blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=False)
    token = models.CharField(max_length=300, null=True,blank=True)
    terminal = models.CharField(max_length=100, null=True,blank=True)

class User2Store(models.Model):
    user_id = models.CharField(max_length=100, null=True,blank=True)
    store_id = models.CharField(max_length=100, null=True,blank=True)

class OrderInfo(models.Model):
    order_id = models.CharField(max_length=100, null=True,blank=True)
    user_id = models.CharField(max_length=100, null=True,blank=True)
    store_id = models.CharField(max_length=100, null=True,blank=True)
    book_id = models.CharField(max_length=100, null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=False)
    number = models.DecimalField(max_digits=10, decimal_places=0, null=True,blank=False)
    state = models.DecimalField(max_digits=1, decimal_places=0, null=True,blank=False)
    order_time = models.DateTimeField(null=True,blank=True)
    payment_time = models.DateTimeField(null=True,blank=True)
    delivery_time = models.DateTimeField(null=True,blank=True)
    receipt_time = models.DateTimeField(null=True,blank=True)