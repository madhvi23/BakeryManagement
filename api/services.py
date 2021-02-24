import json

from api.enum import ResponseConstants, OrderStatus
from api.models import CustomerRegsiteration, Ingredients, BakeryItem, Cart, Order
from api.serializers import BakingItemSerializer
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


def calculateprice(data):
    ingredient = data['ingredientslist']
    sum = 0
    for i in ingredient:
        costprice = Ingredients.objects.get(ingredientname__iexact=i["name"]).costprice
        sum += (int(costprice) * int(i["quantityper"])) / 100
    return sum


def getBakerItemDetail(itemname):
    try:
        data = BakeryItem.objects.get(itemname__iexact=itemname)
        serializer = BakingItemSerializer(data)
        serializeddata = serializer.data
        totalprice = calculateprice(serializeddata)
        serializeddata["sellingprice"] = totalprice + float(serializeddata["makingcharges"])
        serializeddata["costprice"] = totalprice
        del serializeddata["makingcharges"]
        return ResponseConstants.SUCCESS.value, serializeddata
    except Exception as err:
        return ResponseConstants.FAIL.value, str(err)


def getproducts():
    try:
        products = BakeryItem.objects.all()
        serializer = BakingItemSerializer(products, many=True)
        response = list()
        for product in serializer.data:
            item = dict()
            item["price"] = calculateprice(product)
            item["name"] = product["itemname"]
            response.append(item)
        return ResponseConstants.SUCCESS.value, response
    except Exception as err:
        return ResponseConstants.FAIL.value, str(err)


def additems(data):
    customerId = data["customerId"]
    itemname = data["itemname"]
    price = data["price"]
    quantity = data["quantity"]

    customer = CustomerRegsiteration.objects.get(customerId=customerId)
    cartid = Cart.objects.filter(customerId=customer)
    item = [{"itemId": BakeryItem.objects.get(itemname__iexact=itemname).bakeryitemId,
             "quantity": quantity, "price": price}]
    if not cartid:
        Cart.objects.create(customerId=customer, items=item)
        return ResponseConstants.SUCCESS.value
    cartid[0].items.append(item)
    return ResponseConstants.SUCCESS.value


def createorder(data):
    items = data["items"]
    customerId = data["customerId"]
    address = data["address"]
    Order.objects.create(status=OrderStatus.PLACED.value,
                         customerId=customerId, address=address,
                         cartId=Cart.objects.get(customerId__customerId=customerId),
                         items=items)
    print("*"*100)
    return ResponseConstants.SUCCESS.value