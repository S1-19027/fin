# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm
from .services import AuthService, PermissionService
from TransactionUsers.models import TransactionUsers

@require_http_methods(["GET", "POST"])
def register(request):
    """注册视图"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = AuthService.create_user(
                    username=form.cleaned_data['username'],
                    nickname=form.cleaned_data['nickname'],
                    password=form.cleaned_data['password']
                )
                messages.success(request, '注册成功，请登录！')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'注册失败: {str(e)}')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def login(request):
    """登录视图"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = AuthService.authenticate_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                auth_login(request, user)
                messages.success(request, '登录成功！')
                return redirect('/home')
            else:
                messages.error(request, '用户名或密码错误')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def transaction_detail(request, transaction_id):
    """交易详情视图 - 使用权限检查"""
    try:
        transaction = TransactionUsers.objects.get(transaction_id=transaction_id)
        
        # 使用服务层的权限检查
        if not PermissionService.check_transaction_ownership(request.user, transaction):
            messages.error(request, '没有权限查看此交易记录')
            return redirect('transaction_list')
        
        return render(request, 'transaction_detail.html', {'transaction': transaction})
        
    except TransactionUsers.DoesNotExist:
        messages.error(request, '交易记录不存在')
        return redirect('transaction_list')