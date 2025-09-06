from django.db import models
from User.models import User
from Family.models import Family
# Create your models here.
class FamilyMembers(models.Model):
    """家庭-成员关系模型"""
    
    class Role(models.TextChoices):
        ADMIN = "admin", "管理员"
        MEMBER = "member", "普通成员"
    class RelationType(models.TextChoices):
        SELF = "self", "本人"
        FATHER = "father", "父亲"
        MOTHER = "mother", "母亲"
        SON = "son", "儿子"
        DAUGHTER = "daughter", "女儿"
        HUSBAND = "husband", "丈夫"
        WIFE = "wife", "妻子"
        GRANDFATHER = "grandfather", "爷爷"
        GRANDMOTHER = "grandmother", "奶奶"
        GRANDSON = "grandson", "孙子"
        GRANDDAUGHTER = "granddaughter", "孙女"
        OTHER = "other", "其他"
    id = models.AutoField(primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, db_column='family_id', verbose_name="家庭")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', verbose_name="用户")
    relation = models.CharField(max_length=20,choices=RelationType.choices,null=False, verbose_name="关系")
    role = models.CharField(max_length=10, choices=Role.choices, null=False, verbose_name="角色")
    indexes = [
            # 根据family字段的索引 - 提高按家庭查询的效率
            models.Index(fields=["family"]),
            
            # 根据user字段的索引 - 提高按用户查询的效率
            models.Index(fields=["user"]),
            
            # 联合索引 - 提高同时按家庭和用户查询的效率
            models.Index(fields=["family", "user"]),
            
            # 根据角色查询的索引 - 如果需要经常按角色筛选
            models.Index(fields=["role"]),
            
            # 联合索引 - 家庭+角色，用于查询某个家庭的所有管理员等
            models.Index(fields=["family", "role"]),
        ]
    class Meta:
        db_table = 'family_members'
        verbose_name = '家庭成员关系'
        verbose_name_plural = '家庭成员关系'
        unique_together = ('family', 'user')
    def __str__(self):
        return f"{self.user.nickname}在{self.family.family_name}中作为{self.get_relation_display()}（{self.get_role_display()}）"
    def is_admin(self):
        """检查是否为家庭管理员"""
        return self.role == self.Role.ADMIN