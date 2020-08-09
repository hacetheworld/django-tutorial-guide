from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# my USER FORM


# // Customer Model
class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12, null=True)
    profile_pic = models.ImageField(
        default="IMG_20191105_185258_1.jpg", null=True, blank=True)
    email = models.EmailField(max_length=254, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


# // Tags Model
class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


# // Product Model


class Product(models.Model):
    CATEGORY = (('Indoor', 'Indoor'), ('Out Door', 'Out Door'))

    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

# // Order Model


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    STATUS = ((
        'Pending', 'Pending'
    ),
        (
        'Out for delivery', 'Out for delivery'
    ),
        (
        'Deliverd', 'Deliverd'
    ))
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    note = models.CharField(default='Hello World', max_length=100, null=True)
