import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import OrderForm, InterestForm, RegisterForm
from .models import Category, Product, Client, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})


def about(request):
    response = HttpResponse()
    response = render(request, 'myapp/about.html')
    x = request.COOKIES.get('about_visits')
    if x is None:
        x = 1
    else:
        x = int(x)
        x += 1
    response.set_cookie(key='about_visits', value=x, max_age=30)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    prod_list = Product.objects.filter(category__id=cat_no)
    return render(request, 'myapp/detail.html', {'category': category, 'prod_list': prod_list})


def products(request):
    prod_list = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prod_list': prod_list})


def place_order(request):
    msg = ''
    prod_list = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.order_status = 1
                order.status_date = datetime.date.today()
                order.save()
                product = prod_list.get(name=order.product.name)
                product.stock -= order.num_units
                product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prod_list': prod_list})


def product_detail(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)
    msg = ""
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            product.interested += int(form.cleaned_data['interested'])
            product.save()
            response = redirect('/myapp/')
            return response
    else:
        if product.available:
            msg = 'Product is currently available!!! :)'
        else:
            msg = 'Product is not available!!! :('
    form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'product': product, 'msg': msg, 'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return render(request, 'myapp/login.html')
        else:
            return HttpResponse('Registration was unsuccessful')
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    last_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                current_datetime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                request.session['last_login'] = current_datetime
                request.session.set_expiry(3600)
                if last_url == "http://localhost:8000/myapp/orders/":
                    return HttpResponseRedirect(reverse('myapp:orders'))
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def myorders(request):
    msg = ''
    print(request.user.username)
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            return HttpResponse('You are not a registered client!')
        if client:
            order_list = Order.objects.filter(client=client)
            if order_list:
                msg = 'Orders placed by ' + client.first_name + ' ' + client.last_name
            else:
                msg = 'No order placed by ' + client.first_name + ' ' + client.last_name
            return render(request, 'myapp/myorders.html', {'orders': order_list, 'msg': msg})
    else:
        return render(request, 'myapp/login.html')
