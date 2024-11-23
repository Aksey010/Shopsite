from django.core.validators import MaxValueValidator
from django.db import models
from usersapp.models import CiteUser
import datetime
# Create your models here.

# Добавить потом для фильтрации товаров
# class Tag(models.Model):
#     tag = models.CharField(unique=True)


class Shop_item(models.Model):
    name = models.CharField(max_length=30)
    cost = models.CharField(max_length=10)
    image_links = models.SlugField(max_length=100)
    description = models.TextField(default='Продавец не предоставил описания товара.')
    # count_store = models.IntegerField()     Количество на складе
    # tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Basket(models.Model):
    basket_item = models.ForeignKey(Shop_item, on_delete=models.CASCADE)
    user = models.ForeignKey(CiteUser, on_delete=models.CASCADE, blank=True)



class Order(models.Model):
    name = models.CharField(max_length=30, blank=True, default='noname')
    count = models.PositiveIntegerField(validators=[MaxValueValidator(10)], default=1, blank=True)
    full_name = models.CharField(max_length=32)
    email = models.EmailField()
    time = models.DateTimeField(auto_now_add=True)


