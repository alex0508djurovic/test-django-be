from django.urls import path
from .views import search, clear_cache

urlpatterns = [
    path('search/', search, name='search'),
    path('clear-cache/', clear_cache, name='clear_cache'),
]
