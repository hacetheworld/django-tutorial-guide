from django.urls import path
# // Views
from .views import Home


# Urls
urlpatterns = [
    path("", Home)
]
