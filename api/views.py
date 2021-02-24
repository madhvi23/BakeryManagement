from api.enum import HttpConstants, ResponseConstants
from api.services import userregisteration, addingredient, addbakeryitem, \
    getBakerItemDetail, getproducts, additems, createorder, getorders

from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.serializers import RegistrationSerializer, IngredientSerializer, BakingItemSerializer


USER_CREATED_MESSAGE = "User Created Successfully!!"
LOGIN_MESSAGE = "User Logged in Successfully"
INGREDIENT_ADDED_MESSAGE = 'Ingredient Added Successfully!!'
BAKERYITEM_ADDED_MESSAGE = 'Bakery Item Added Successfully!!'
ITEM_ADDED_MESSAGE = 'Item added to cart!!'
ORDER_PLACED_MESSAGE = 'Order Placed Successfully!!'


@api_view([HttpConstants.POST.value])
def registeration(request):
    if request.method == HttpConstants.POST.value:
        try:
            serializer = RegistrationSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            response = userregisteration(serializer.data)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"status": HTTP_201_CREATED, "message": USER_CREATED_MESSAGE})
            raise Exception("Error While Regsitering User")
        except Exception as err:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": str(err)})


@api_view([HttpConstants.POST.value])
def loginview(request):
    if request.method == HttpConstants.POST.value:
        try:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            user = authenticate(username=username, password=password)
            if user:
                return Response({"status": HTTP_200_OK, "message": LOGIN_MESSAGE})
            raise Exception("Username or Password Incorrect")
        except Exception as err:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": str(err)})



@api_view([HttpConstants.POST.value])
@permission_classes([IsAdminUser, IsAuthenticated])
def ingredient(request):
    if request.method == HttpConstants.POST.value:
        try:
            serializer = IngredientSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            response = addingredient(serializer.data)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"status": HTTP_201_CREATED, "message": INGREDIENT_ADDED_MESSAGE})
        except Exception as err:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": str(err)})


@api_view([HttpConstants.POST.value, HttpConstants.GET.value])
@permission_classes([IsAdminUser, IsAuthenticated])
def bakingitems(request, item=None):
    if request.method == HttpConstants.POST.value:
        try:
            serializer = BakingItemSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            response = addbakeryitem(serializer.data)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"status": HTTP_201_CREATED, "message": BAKERYITEM_ADDED_MESSAGE})
        except Exception as err:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": str(err)})

    if request.method == HttpConstants.GET.value:
        response, data = getBakerItemDetail(item)
        if response == ResponseConstants.SUCCESS.value:
            return Response({"data": data, "status": HTTP_200_OK})
        return Response({"Error": data, "status": HTTP_400_BAD_REQUEST})


@api_view([HttpConstants.GET.value])
def getallproducts(request):
    response, data = getproducts()
    if response == ResponseConstants.SUCCESS.value:
        return Response({"data": data, "status": HTTP_200_OK})
    return Response({"Error": data, "status": HTTP_400_BAD_REQUEST})


@api_view([HttpConstants.POST.value])
def additemtocart(request):
    try:
        response = additems(request.data)
        if response == ResponseConstants.SUCCESS.value:
            return Response({"message": ITEM_ADDED_MESSAGE, "status": HTTP_201_CREATED})
    except Exception as err:
        return Response({"Error": str(err), "status": HTTP_400_BAD_REQUEST})


@api_view([HttpConstants.GET.value, HttpConstants.POST.value])
def order(request, customerId=None):
    if request.method == HttpConstants.POST.value:
        try:
            response, orderId = createorder(request.data)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"message": ORDER_PLACED_MESSAGE, "status": HTTP_201_CREATED, "orderId": orderId})
        except Exception as err:
            return Response({"Error": str(err), "status": HTTP_400_BAD_REQUEST})

    if request.method == HttpConstants.GET.value:
        try:
            response, orders = getorders(customerId)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"orders": orders, "status": HTTP_200_OK})
        except Exception as err:
            return Response({"Error": str(err), "status": HTTP_400_BAD_REQUEST})



