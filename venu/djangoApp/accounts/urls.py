from django.urls import path
# // Views
from .views import Home, customer, products, createOrder, updateOrder, deleteOrder


# Urls
urlpatterns = [
    path("", Home, name='home'),
    path("customer/<int:customer_id>", customer, name='customer'),
    path("products", products, name='products'),
    path("create_order/<int:c_id>", createOrder, name='create_order'),
    path("update_order/<int:order_id>", updateOrder, name='update_order'),
    path("delete_order/<int:order_id>", deleteOrder, name='delete_order')
]
