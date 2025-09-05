
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django import forms
from .models import User

# 登录表单
class LoginForm(forms.Form):
	username = forms.CharField(label='用户名', max_length=50)
	password = forms.CharField(label='密码', widget=forms.PasswordInput)

# 注册表单
class RegisterForm(forms.ModelForm):
	password = forms.CharField(label='密码', widget=forms.PasswordInput)
	password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
	role = forms.ChoiceField(label='角色', choices=User.Role.choices)
    

	class Meta:
		model = User
		fields = ['username', 'email', 'nickname', 'password', 'role']

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		password2 = cleaned_data.get('password2')
		if password and password2 and password != password2:
			raise forms.ValidationError('两次输入的密码不一致')
		return cleaned_data

# 注册视图
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.role = form.cleaned_data['role']
			user.save()
			messages.success(request, '注册成功，请登录！')
			return redirect('login')
	else:
		form = RegisterForm()
	return render(request, 'register.html', {'form': form})

# 登录视图
def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, '登录成功！')
				return redirect('/')  # 登录后跳转主页，可自定义
			else:
				messages.error(request, '用户名或密码错误')
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})
