from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Ingredients

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True, trim_whitespace=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    firstname = serializers.CharField(max_length=100, trim_whitespace=True, required=True)
    lastname = serializers.CharField(max_length=100, trim_whitespace=True)
    email = serializers.CharField(max_length=100, required=True, trim_whitespace=True)
    gender = serializers.CharField(max_length=8, required=True, trim_whitespace=True)
    mobileno = serializers.CharField(max_length=10, required=True, trim_whitespace=True)
    countrycode = serializers.CharField(max_length=5, required=True, trim_whitespace=True)
    password = serializers.CharField(max_length=10, required=True)


class IngredientSerializer(serializers.Serializer):
    ingredientname = serializers.CharField(max_length=100, required=True,
                                           validators=[UniqueValidator(queryset=Ingredients.objects.all())])
    description = serializers.CharField(max_length=100)
    costprice = serializers.CharField(required=True)
    category = serializers.CharField(max_length=100)


class BakingItemSerializer(serializers.Serializer):
    itemname = serializers.CharField(max_length=100, required=True)
    makingcharges = serializers.CharField(required=True, max_length=100)
    ingredientslist = serializers.JSONField(required=True)

