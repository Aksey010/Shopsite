from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Shop_item, Basket, Order
from .forms import BasketForm, OrderForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, TemplateView, DetailView, DeleteView
import datetime


# Create your views here.


class IndexView(ListView):
    template_name = 'shop/index.html'
    model = Shop_item
    paginate_by = 24

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            object_list = Shop_item.objects.all()
        else:
            object_list = Shop_item.objects.filter(Q(name__icontains=query.upper()))
        return object_list

class ResultIndexView(ListView):
    template_name = 'shop/results.html'
    model = Shop_item

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            object_list = Shop_item.objects.all()
        else:
            object_list = Shop_item.objects.filter(Q(name__icontains=query.upper()))
        return object_list


class AboutView(TemplateView):
    template_name = 'shop/about.html'


class ItemView(DetailView):
    template_name = 'shop/item.html'
    model = Shop_item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BasketForm
        return context


class BasketItemCreateView(CreateView):
    model = Shop_item
    template_name = ''
    success_url = '/'
    form_class = BasketForm

    def post(self, request, *args, **kwargs):
        self.Shop_item_pk = kwargs['pk']
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        basket_item_id = get_object_or_404(Shop_item, pk=self.Shop_item_pk).id
        form.instance.basket_item_id = basket_item_id
        return super().form_valid(form)


class ListBasket(ListView):
    model = Basket
    template_name = 'shop/basket.html'
    paginate_by = 8

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user).select_related('basket_item').all()


class DeleteBasketView(DeleteView):
    model = Basket
    template_name = 'shop/delete_basket.html'
    success_url = reverse_lazy('shop:basket')


def OrderView(request):
    object_list = Basket.objects.filter(user=request.user).select_related('basket_item').all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = request.POST.items()

            full_name = request.POST['full_name']
            email = request.POST['email']

            for name, value in data:
                    if name.startswith('product_in_basket_'):
                        if int(value) > 0:
                            product_in_basket_id = name.split("product_in_basket_")[1]
                            product_in_basket = Basket.objects.get(id=product_in_basket_id)

                            order = Order.objects.create(name=product_in_basket.basket_item.name, count=value, full_name=full_name, email=email, time=datetime.datetime.now())
                            order.save(force_update=True)
                            product_in_basket.delete()


            return HttpResponseRedirect(reverse('shop:index'))
        else:
            return render(request, 'shop/order.html', context={'form': form, 'object_list': object_list})
    else:
        form = OrderForm()
        return render(request, 'shop/order.html', locals())

