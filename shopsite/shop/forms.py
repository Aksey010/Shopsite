from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Basket, Order, Shop_item


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ()


class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=32, label='ФИО')
    email = forms.EmailField(label='Почта')


