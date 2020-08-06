from django.contrib import admin

from .models import Customer, Order, Product, Tag
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    """
    Customer Admin
    """
    list_display = ['name', 'email', 'phone']


class OrderAdmin(admin.ModelAdmin):
    """
    Order Admin
    """
    list_display = ['id', 'product', 'customer', 'status']


class ProductAdmin(admin.ModelAdmin):
    """
    Customer Admin
    """
    list_display = ['name', 'price', 'category', 'description']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
admin.site.register(Tag)
admin.site.register(Product, ProductAdmin)
