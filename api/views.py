from api.enum import HttpConstants, ResponseConstants
from api.services import userregisteration, addingredient, addbakeryitem

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


@api_view([HttpConstants.POST.value])
@permission_classes([IsAdminUser, IsAuthenticated])
def bakingitems(request):
    if request.method == HttpConstants.POST.value:
        try:
            serializer = BakingItemSerializer(data=request.POST)
            serializer.is_valid(raise_exception=True)
            response = addbakeryitem(serializer.data)
            if response == ResponseConstants.SUCCESS.value:
                return Response({"status": HTTP_201_CREATED, "message": INGREDIENT_ADDED_MESSAGE})
        except Exception as err:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": str(err)})




