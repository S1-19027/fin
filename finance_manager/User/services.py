# services.py
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
from .models import User
from FamilyMembers.models import FamilyMembers

class AuthService:
    """认证相关服务"""
    
    @staticmethod
    def authenticate_user(username, password):
        """用户认证"""
        return authenticate(username=username, password=password)
    
    @staticmethod
    @transaction.atomic
    def create_user(username, nickname, password):
        """创建用户"""
        user = User(
            username=username,
            nickname=nickname,
            password=make_password(password)
        )
        user.save()
        return user

class PermissionService:
    """权限检查服务"""
    
    @staticmethod
    def check_transaction_ownership(user, transaction):
        """
        检查用户是否有权限访问指定的交易记录
        :param user: 当前登录用户
        :param transaction: 交易记录实例
        :return: 布尔值，表示用户是否有权限
        """
        # 如果是家庭管理员，可以访问其家庭成员创建的交易记录
        if PermissionService.is_family_admin(user, transaction.family):
            return True
        
        # 普通用户只能访问自己创建的交易记录
        return transaction.creator == user
    
    @staticmethod
    def is_family_admin(user, family):
        """检查用户是否是某个家庭的管理员"""
        try:
            membership = FamilyMembers.objects.get(
                family=family,
                user=user,
                role=FamilyMembers.Role.ADMIN
            )
            return True
        except FamilyMembers.DoesNotExist:
            return False