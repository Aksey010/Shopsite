from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('results/', views.ResultIndexView.as_view(), name='results'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('item/<int:pk>', views.ItemView.as_view(), name='item'),
    path('basket/', views.ListBasket.as_view(), name='basket'),
    path('basket-item-create/<int:pk>', views.BasketItemCreateView.as_view(), name='basket-item-create'),
    path('basket-item-delete/<int:pk>', views.DeleteBasketView.as_view(), name='basket-item-delete'),
    path('order/', views.OrderView, name='order'),
]
