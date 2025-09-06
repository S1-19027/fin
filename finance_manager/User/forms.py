# forms.py
from django import forms
from .models import User

class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    """注册表单"""
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'nickname', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return cleaned_data

    def save(self, commit=True):
        """重写save方法，使用服务层创建用户"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user