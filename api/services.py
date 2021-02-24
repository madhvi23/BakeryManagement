import json

from api.enum import ResponseConstants, OrderStatus
from api.models import CustomerRegsiteration, Ingredients, BakeryItem, Cart, Order
from api.serializers import BakingItemSerializer, OrderSerializer
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
    bakeryitemId = data["itemId"]
    price = data["price"]
    quantity = data["quantity"]

    customer = CustomerRegsiteration.objects.get(customerId=customerId)
    cartid = Cart.objects.filter(customerId=customer)
    item = [{"itemname": BakeryItem.objects.get(pk=bakeryitemId).itemname,
             "quantity": quantity, "price": price}]

    if not cartid:
        Cart.objects.create(customerId=customer, items=item)
        return ResponseConstants.SUCCESS.value
    cartid[0].items.extend(item)
    cartid[0].save(update_fields=['items'])
    return ResponseConstants.SUCCESS.value


def createorder(data):
    customerId = data["customerId"]
    address = data["address"]
    customer = CustomerRegsiteration.objects.get(pk=customerId)
    cart = Cart.objects.get(customerId=customer)
    items = cart.items
    total = 0
    print(cart.items)

    if not items:
        raise Exception("Cart is Empty!!")

    for item in items:
        total += item["price"]*item["quantity"]

    order = Order.objects.create(status=OrderStatus.PLACED.value,
                         customerId=customer, address=address,
                         cartId=cart,
                         items=items, total=total)
    cart.items = []
    cart.save(update_fields=['items'])
    return ResponseConstants.SUCCESS.value, order.orderId


def getorders(customerId):
    orders = Order.objects.filter(customerId=CustomerRegsiteration.objects.get(pk=customerId))
    serializer = OrderSerializer(orders, many=True)
    print(serializer.data)
    return ResponseConstants.SUCCESS.value, serializer.data