import email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib.auth import logout
from .models import CustomUser



def home(request):
    return render(request, 'home.html')


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
            elif phone =="":
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
                           username=email ,email=email, first_name=name,phone=phone, password=password1)                      
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


    