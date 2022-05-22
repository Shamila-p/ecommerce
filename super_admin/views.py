from email import message
from typing import NamedTuple
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from super_admin.models import Category
from super_admin.models import Product
from user.models import CustomUser


def index(request):
    return redirect('/admin/login')


def login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin/dashboard')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "":
            messages.info(request, 'username field cannot be empty!!')
        elif password == "":
            messages.info(request, 'password field cannot be empty!!')
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                auth.login(request, user)
                return redirect('/admin/dashboard')
            else:
                messages.info(request, 'username/password incorrect!!')
        return redirect('/admin/login')
    else:
        return render(request, 'admin_login.html')


def logout(request):
    auth.logout(request)
    return redirect('/admin/login')


def dashboard(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    return render(request, 'dashboard.html')


def user(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    users = CustomUser.objects.filter(is_superuser=False)
    return render(request, 'user.html', {'users': users})


def add_user(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
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
                    return redirect('/admin/add-user')
                else:
                    CustomUser.objects.create_user(
                        username=email, email=email, first_name=name, phone=phone, password=password1)
                    print('user create')
                    return redirect('/admin/user')
            else:
                messages.info(request, 'password not matching')
    return render(request, 'add_user.html')


def edit_user(request, user_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST["email"]
        phone = request.POST["phone"]
        user = CustomUser.objects.get(id=user_id)
        if name == "":
            messages.info(request, 'name field cannot be empty!!')
        elif email == "":
            messages.info(request, 'email field cannot be empty!!')
        elif phone == "":
            messages.info(request, 'phone no field cannot be empty!!')
        elif user.email != email and CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'email already registerd!!')
        else:
            user.email = email
            user.phone = phone
            user.save()
            return redirect('/admin/user')
        return redirect('/admin/user/edit/'+str(user_id))

    else:
        user = CustomUser.objects.get(id=user_id)
        return render(request, 'edit_user.html', {'user': user})


def delete_user(request, user_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return redirect('/admin/user')


def block_user(request, user_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        user = CustomUser.objects.get(id=user_id)
        # if user.is_active == True:
        #     user.is_active = False
        # else:
        #     user.is_active = True
        user.is_active = not user.is_active
        user.save()
        return redirect('/admin/user')


def category(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})


def add_category(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        print('category create')
        return redirect('/admin/category')
    else:
        return render(request, 'add_category.html')


def edit_category(request, category_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
        category = Category.objects.get(id=category_id)
        category.name = name
        category.save()
        return redirect('/admin/category')

    else:
        category = Category.objects.get(id=category_id)
        return render(request, 'edit_category.html', {'category': category})


def delete_category(request, category_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        category = Category.objects.get(id=category_id)
        category.delete()
        return redirect('/admin/category')


def product(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


def add_product(request):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        image = request.FILES['image']
        Product.objects.create(name=name, description=description, price=price,
                               quantity=quantity, category_id=category_id, image=image)
        return redirect('/admin/product')
    else:
        categories = Category.objects.all()
        return render(request, 'add_product.html', {'categories': categories})


def edit_product(request, product_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        image = request.FILES.get('image')
        print(image)
        product = Product.objects.get(id=product_id)
        product.name = name
        product.description = description
        product.price = price
        product.quantity = quantity
        product.category_id = category_id
        if image is not None:
            product.image = image
        product.save()
        return redirect('/admin/product')
    else:
        categories = Category.objects.all()
        product = Product.objects.get(id=product_id)
        return render(request, 'edit_product.html', {'product': product, 'categories': categories})


def delete_product(request, product_id):
    if not(request.user.is_authenticated and request.user.is_superuser):
        return redirect('/admin/login')
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('/admin/product')

