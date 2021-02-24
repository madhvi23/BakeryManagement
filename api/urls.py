from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path('register/', registeration),
    path('login/', loginview),
    path('addingredient/', ingredient),
    path('bakeryitems/', bakingitems),
    path('bakeryitems/<str:item>/', bakingitems),
    path('products/', getallproducts),
    path('additem/', additemtocart),
    path('placeorder/', order),
    path('placeorder/<int:customerId>/', order)
]
