from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields import SlugField
from django.urls import reverse  
from accounts.models import * 
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    def get_url(self):
        return reverse('store', args=[self.slug])

    def __str__ (self):
        return self.category_name

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__ (self):
        return self.product_name

class ImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    image = models.ImageField(upload_to='store/products',max_length=255)

    def __str__(self):
        return self.product.product_name

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.TextField(max_length=500)
    rating = models.FloatField()
    created_date = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.title

