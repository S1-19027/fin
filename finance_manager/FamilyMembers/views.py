from django.shortcuts import render
from django.db import transaction
from .models import Family, FamilyMembers
from OperationLog.models import OperationLog
# Create your views here.   
"""
创建家庭，创建者自动设置为家庭管理员
"""
@staticmethod
@transaction.atomic

def create_family(user, family_name, relation="创建者"):
        """
        创建家庭并成为管理员
        """
        # 1. 创建家庭
        family = Family.objects.create(family_name=family_name)
        
        # 2. 将创建者设置为家庭管理员
        membership = FamilyMembers.objects.create(
            family=family,
            user=user,
            relation=relation,
            role=FamilyMembers.Role.ADMIN
        )
        
        # 3. 记录操作日志
        OperationLog.objects.create(
            user=user,
            operation_type="create_family",
            operation_content=f"创建家庭 '{family_name}' 并成为管理员"
        )
        
        return family, membership
# services.py
"""
加入现有家庭，作为普通成员
"""
@staticmethod
@transaction.atomic
def join_family(user, family_id, relation):
        """
        加入现有家庭作为普通成员
        """
        family = Family.objects.get(family_id=family_id)
        
        # 检查是否已是成员
        if FamilyMembers.objects.filter(family=family, user=user).exists():
            raise ValueError("已是该家庭成员")
        
        # 加入为普通成员
        membership = FamilyMembers.objects.create(
            family=family,
            user=user,
            relation=relation,
            role=FamilyMembers.Role.MEMBER
        )
        
        # 记录操作日志
        OperationLog.objects.create(
            user=user,
            operation_type="join_family",
            operation_content=f"加入家庭 '{family.family_name}' 作为普通成员"
        )
        
        return membership
class PermissionService:
    
    @staticmethod
    def can_create_family(user):
        """检查用户是否可以创建家庭"""
        # 现在所有注册用户都可以创建家庭
        return True
    
    @staticmethod
    def is_family_admin(user, family_id):
        """检查用户是否是某个家庭的管理员"""
        return FamilyMembers.objects.filter(
            family_id=family_id,
            user=user,
            role=FamilyMembers.FamilyRole.ADMIN
        ).exists()
    
    @staticmethod
    def get_user_role_in_family(user, family_id):
        """获取用户在特定家庭中的角色"""
        try:
            membership = FamilyMembers.objects.get(
                family_id=family_id,
                user=user
            )
            return membership.role
        except FamilyMembers.DoesNotExist:
            return None