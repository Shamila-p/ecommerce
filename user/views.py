from datetime import date, datetime
from distutils.log import log
import email
from email.mime import image
from itertools import product
from unicodedata import name
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth import logout
from .models import Cart, CustomUser, Order
from super_admin.models import Product
from django.contrib.auth.decorators import login_required
from datetime import datetime


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def view_more(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_view.html', {'product': product})


@login_required
def user_profile(request):
    return render(request, 'user_profile.html')


def user_edit(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        image = request.FILES.get('image')
        user = CustomUser.objects.get(id=request.user.id)
        user.first_name = name
        user.email = email
        user.phone = phone
        if image is not None:
            user.profile_image = image
        user.save()
        return redirect('/user/profile')


def change_password(request):
    if request.method == 'POST':
        current = request.POST['currentpoassword']
        new = request.POST['newpassword']
        confirm = request.POST['confirmpassword']
        user = CustomUser.objects.get(id=request.user.id)

        if new != confirm:
            messages.info(request, 'password not matching')
        elif not user.check_password(current):
            messages.info(request, 'wrong current password')
        else:
            user.set_password(new)
            user.save()
        return redirect('/user/profile')


@login_required
def cart(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user_id=request.user.id)
        total_price = 0
        for cart_item in cart_items:
            total_price = total_price + cart_item.total_price
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def cart_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login?next=/product/view/'+str(product_id))
    if request.method == "POST":
        user_id = request.user.id
        product_id = product_id
        if Cart.objects.filter(product_id=product_id, user_id=user_id).exists():
            cart_item = Cart.objects.get(
                product_id=product_id, user_id=user_id)
            cart_item.quantity += 1
            cart_item.save()

        else:
            quantity = 1
            Cart.objects.create(quantity=quantity,
                                user_id=user_id, product_id=product_id)
        # return redirect('/product/view/'+str(product_id))
        return redirect('/cart')


@login_required
def quantity_add(request, cart_item_id):
    if request.method == 'POST':
        cart_item = Cart.objects.get(id=cart_item_id)

        if cart_item.quantity < cart_item.product.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.info(request, 'Stock limit reached')
        return redirect('/cart')


@login_required
def quantity_minus(request, cart_item_id):
    if request.method == 'POST':
        cart_item = Cart.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('/cart')


@login_required
def remove_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = Cart.objects.get(id=cart_item_id)
        cart_item.delete()
        return redirect('/cart')


@login_required
def check_out(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user_id=request.user.id)
        total_price = 0
        for cart_item in cart_items:
            total_price = total_price + cart_item.total_price
        return render(request, 'order.html', {'cart_items': cart_items, 'total_price': total_price})
    if request.method == 'POST':

        address = request.POST['address']
        cart_items = Cart.objects.filter(user_id=request.user.id)
        for cart_item in cart_items:
            product_id = cart_item.product_id
            quantity = cart_item.quantity
            total_price = cart_item.total_price
            date_time = datetime.now()
            Order.objects.create(user_id=request.user.id, product_id=product_id, quantity=quantity,
                                 address=address, total_price=total_price, ordered_date=date_time)
        cart_items.delete()
        return redirect('/')

@login_required
def order(request):
    if request.method=='GET':
        orders=Order.objects.filter(user_id=request.user.id)
        return render(request,'order_view.html',{'orders':orders})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            if email == "":
                messages.info(request, 'email field cannot be empty!!')
            elif password == "":
                messages.info(request, 'password field cannot be empty!!')
            else:
                user = auth.authenticate(username=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect_after_login(request)
                else:
                    messages.info(request, 'email/password incorrect!!')
            return redirect('/login')
        else:
            return render(request, 'login.html')


def redirect_after_login(request):
    nxt = request.POST.get("next", None)
    print(nxt)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if name == "":
                messages.info(request, 'name field cannot be empty!!')
            elif email == "":
                messages.info(request, 'email field cannot be empty!!')
            elif phone == "":
                messages.info(request, 'phone no field cannot be empty!!')
            elif password1 == "":
                messages.info(request, 'password field cannot be empty!!')
            elif password2 == "":
                messages.info(request, 'password field cannot be empty!!')
            else:
                if password1 == password2:
                    if CustomUser.objects.filter(email=email).exists():
                        messages.info(request, 'email taken')
                        return redirect('/signup')
                    else:
                        CustomUser.objects.create_user(
                            username=email, email=email, first_name=name, phone=phone, password=password1)
                        print('user created')
                        return redirect('/login')
                else:
                    messages.info(request, 'password not matching')
            return redirect('/signup')
        else:
            return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
