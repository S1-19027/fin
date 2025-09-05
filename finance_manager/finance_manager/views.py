from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.contrib import auth
from django.contrib.auth.models import User


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        # if 验证成功返回 user 对象，否则返回None
        user = auth.authenticate(username=user, password=pwd)

        if user:
            # request.user ： 当前登录对象
            auth.login(request, user)
            # return HttpResponse("OK")
            return redirect("/auth/index")

    return render(request, "auth/login.html")
