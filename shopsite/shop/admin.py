from django.contrib import admin
from .models import Shop_item, Basket, Order
# Register your models here.

admin.site.register(Shop_item)
admin.site.register(Basket)
admin.site.register(Order)
