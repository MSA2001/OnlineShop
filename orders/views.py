from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from django.http import HttpResponse
import requests
import json


# Create your views here.


class CartView(View):

    def get(self, request):
        cart = Cart(request)

        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):

    def get(self, request):
        pass

    def post(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                     quantity=item['quantity'])

        cart.clear()
        return redirect('orders:order_detail', order.id)


# zarin pal https://github.com/rasooll/zarinpal-django-py3/blob/master/views.py
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://localhost:8000/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

