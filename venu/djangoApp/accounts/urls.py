from django.urls import path
# // Views
from .views import Home, customer, products


# Urls
urlpatterns = [
    path("", Home),
    path("customers", customer),
    path("products", products)
]
