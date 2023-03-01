from django.db import models
from django.contrib.auth.models import User


class Ingredients(models.Model):
    ingredientId = models.AutoField(primary_key=True)
    ingredientname = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    costprice = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ingredientname


class BakeryItem(models.Model):
    bakeryitemId = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=100, blank=False, null=False)
    makingcharges = models.CharField(max_length=100)
    ingredientslist = models.JSONField()

    def __str__(self):
        return self.itemname


class CustomerRegsiteration(models.Model):
    customerId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=8)
    mobileno = models.CharField(max_length=10, null=False, blank=False)
    countrycode = models.CharField(max_length=5, null=False, blank=False)
    role = models.CharField(max_length=10, default='Customer')

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    cartId = models.AutoField(primary_key=True)
    customerId = models.OneToOneField(CustomerRegsiteration, on_delete=models.CASCADE)
    items = models.JSONField(default=[])


class Order(models.Model):
    orderId = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    customerId = models.OneToOneField(CustomerRegsiteration, on_delete=models.CASCADE)
    cartId = models.OneToOneField(Cart, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20)
    total = models.IntegerField(default=0)
    items = models.JSONField(default={})

    def __str__(self):
        return self.orderId


class TestForRebase(models.Model):
    pass

class TestForRebase2(models.Model):
    pass

class TestForRebase3(models.Model):
    pass

class Order1(models.Model):
    pass

