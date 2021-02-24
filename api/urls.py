from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path('register/', registeration),
    path('login/', loginview),
    path('addingredient/', ingredient),
    path('bakeryitems/', bakingitems),
]
