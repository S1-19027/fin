from django.db import models

# Create your models here.
# 家庭模型
class Family(models.Model):
    family_id = models.AutoField(primary_key=True, verbose_name="家庭ID")
    family_name = models.CharField(max_length=100, verbose_name="家庭名称")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'family'
        verbose_name = '家庭'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.family_name
