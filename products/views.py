from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'products/home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'products/product.html'


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists:
            order_item.quantity += 1
            order_item.save()
        else:
            order.item.add(order_item)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(order_item)

    return redirect("product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists:
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)
            if order_item:
                order_item[0].delete()
        else:
            return redirect("product", slug=slug)
    else:
        return redirect("product", slug=slug)

    return redirect("product", slug=slug)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordconfirm = request.POST['passwordconfirm']

        try:
            user = User.objects.get(username=username)
            return render(request, 'products/register', {'error': 'User already exsists'})
        except User.DoesNotExist:
            if password != passwordconfirm:
                return render(request, 'products/register', {'error': 'Passwords do not match'})
            user = User.objects.create_user(
                username=username, email=email, password=password)
            auth.login(request, user)
            return redirect('index')
    else:
        return render(request, 'products/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, "products/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, 'products/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')
