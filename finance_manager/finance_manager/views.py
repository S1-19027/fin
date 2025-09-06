from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.contrib import auth
from django.contrib.auth.models import User

def index(request):
    return redirect("login")

