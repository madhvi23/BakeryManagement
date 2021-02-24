from api.enum import ResponseConstants
from api.models import CustomerRegsiteration, Ingredients, BakeryItem
from django.contrib.auth.models import User


def userregisteration(data):
    username = data["username"]
    password = data["password"]
    firstname = data["firstname"]
    lastname = data["lastname"]
    mobileno = data["mobileno"]
    gender = data["gender"]
    email = data["email"]
    countrycode = data["countrycode"]

    #TODO: create serializer and add validators
    user = User.objects.create(email=email, username=username, first_name=firstname,
                               last_name=lastname)
    user.set_password(password)
    user.save(update_fields=['password'])
    CustomerRegsiteration.objects.create(user=user, gender=gender, mobileno=mobileno, countrycode=countrycode)
    return ResponseConstants.SUCCESS.value


def addingredient(data):
    ingedientname = data["ingredientname"]
    description = data['description']
    category = data['category']
    costprice = data['costprice']

    Ingredients.objects.create(
        ingredientname=ingedientname, description=description, category=category, costprice=costprice
    )
    return ResponseConstants.SUCCESS.value


def addbakeryitem(data):
    try:

        bakeryitemname = data["itemname"]
        makingcharge = data['makingcharges']
        ingredientlist = data["ingredientslist"]

        BakeryItem.objects.create(
            itemname=bakeryitemname, makingcharges=makingcharge, ingredientslist=ingredientlist
        )

        return ResponseConstants.SUCCESS.value
    except Exception as err:
        raise Exception(str(err))
