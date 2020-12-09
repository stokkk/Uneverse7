from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . forms import RegistrationForm, LogInForm

from django.views.generic import View, DetailView

# Create your views here.

def indexView(request):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT b.brand_name, p.name, p.description, p.price, p.discount, ct.name, cs.country_name 
    FROM Products as p, Categories as ct, Countries as cs, Brands as b
    WHERE p.category_id = ct.ID AND p.country_id = cs.id AND p.brand = b.brand_id
    ORDER BY p.name ASC
    """)
    products = cursor.fetchall()
    return render(request, 'home/index.html', {'products': products, 'user': request.user})


def LogInView(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        print(request.POST)
        if form.is_valid():
            login_ = request.POST['login']
            pass_ = request.POST['password']

            user = authenticate(username=login_, password=pass_)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect("/")
            else:
                render(request, 'home/LogIn.html', {'form': form, 'badauth': 'bad authentification!!!'})
    else:
        form = LogInForm()
    return render(request, 'home/LogIn.html', {'form': form})


class RegistrationView(View):


    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'home/Registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            login_ = request.POST['login']
            pass_ = request.POST['password']
            try:
                user = User.objects.get(username=login_)
                return render(request, 'home/Registration.html', {'form': form, 'user_exist': True})
            except User.DoesNotExist:
                print("(DoesNotExist) пользователя с именем %s небыло найдено" % login_)
                user = User.objects.create_user(username=login_,password=pass_)
                user.save()
                return HttpResponseRedirect("/login/")
        return render(request, 'home/Registration.html', {'form': form, 'badregist': "registration fallen!"})



def LogOutView(request):
    logout(request)
    return HttpResponseRedirect("/")