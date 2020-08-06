from django.db import models

# Create your models here.


# // Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=254, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


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
