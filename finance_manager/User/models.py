# models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.utils import timezone
from Family.models import Family


class CustomUserManager(BaseUserManager):
    """自定义用户管理器，用于创建用户和超级用户"""

    def create_user(self, username, password=None, **extra_fields):
        """
        创建并保存一个普通用户
        """
        if not username:
            raise ValueError("用户必须设置用户名")

        user = self.model(username=username,  **extra_fields)
        user.set_password(password)  # 加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username,password=None, **extra_fields):
        """
        创建并保存一个超级用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # 创建超级用户时，默认赋予管理员角色
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置 is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置 is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户模型，去除全局角色，仅保留基础信息
    """
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="用户名",
        # help_text="用于登录系统的唯一标识",
    )
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱地址")
    nickname = models.CharField(
        max_length=100, verbose_name="昵称", #help_text="在系统中显示的名称"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="头像"
    )
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="加入时间")
    last_login = models.DateTimeField(
        blank=True, null=True, verbose_name="最后登录时间"
    )
    is_active = models.BooleanField(default=True, verbose_name="激活状态")
    is_staff = models.BooleanField(
        default=False, verbose_name="管理员状态", help_text="是否可以登录管理后台"
    )
    is_superuser = models.BooleanField(default=False, verbose_name="超级用户状态")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    objects = models.Manager()  # 使用默认管理器

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = "用户管理"
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            # models.Index(fields=["family"]),  # 联合索引，提高查询效率
        ]

    def __str__(self):
        return f"{self.nickname} ({self.username})"

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # --- 简化的权限检查方法 ---
    def is_admin(self):
        """用户是否是管理员"""
        return self.role == self.Role.ADMIN

    def is_member(self):
        """用户是否是普通成员"""
        return self.role == self.Role.MEMBER

    # 基于角色的复合权限检查
    def can_manage_family(self):
        """是否可以管理家庭信息（只有管理员可以）"""
        return self.is_admin()

    def can_manage_members(self):
        """是否可以管理家庭成员（只有管理员可以）"""
        return self.is_admin()

    def can_view_all_transactions(self):
        """是否可以查看所有成员的交易记录（只有管理员可以）"""
        return self.is_admin()

    def can_edit_any_transaction(self):
        """是否可以编辑任何交易记录（只有管理员可以）"""
        return self.is_admin()

    def can_manage_categories(self):
        """是否可以管理分类（只有管理员可以）"""
        return self.is_admin()

    def can_manage_payment_methods(self):
        """是否可以管理支付方式（只有管理员可以）"""
        return self.is_admin()

    def can_view_global_stats(self):
        """是否可以查看全局统计（只有管理员可以）"""
        return self.is_admin()

    # 所有用户都有的权限
    def can_view_own_transactions(self):
        """是否可以查看自己的交易记录（所有用户都可以）"""
        return True

    def can_edit_own_transactions(self):
        """是否可以编辑自己的交易记录（所有用户都可以）"""
        return True

    def can_manage_own_tags(self):
        """是否可以管理自己的标签（所有用户都可以）"""
        return True

    def can_view_personal_stats(self):
        """是否可以查看个人统计（所有用户都可以）"""
        return True
