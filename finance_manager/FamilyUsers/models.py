from django.db import models

# Create your models here.
class FamilyMembers(models.Model):
    """家庭-成员关系模型"""
    
    class Role(models.TextChoices):
        ADMIN = "admin", "管理员"
        MEMBER = "member", "普通成员"
    
    id = models.AutoField(primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, db_column='family_id', verbose_name="家庭")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', verbose_name="用户")
    relation = models.CharField(max_length=20, verbose_name="关系")
    role = models.CharField(max_length=10, choices=Role.choices, null=False, verbose_name="角色")

    class Meta:
        db_table = 'family_members'
        verbose_name = '家庭成员关系'
        verbose_name_plural = '家庭成员关系'
        unique_together = ('family', 'user')

    def __str__(self):
        return f"{self.user.nickname} - {self.family.family_name}"