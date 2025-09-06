from django.db import models
from Transaction.models import Transaction
from User.models import User
from Family.models import Family
# Create your models here.

# 标签模型
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True, verbose_name="标签ID")
    name = models.CharField(max_length=50, verbose_name="标签名称")
    color = models.CharField(max_length=7, default='#808080', verbose_name="颜色")
    transaction = models.ForeignKey(Transaction, null=True,on_delete=models.CASCADE, db_column='transaction_id', verbose_name="交易")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id',verbose_name="创建者")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, db_column='family_id',verbose_name="所属家庭")

    class Meta:
        db_table = 'tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        unique_together = ('name', 'family')  # 同一家庭下标签名唯一

    def __str__(self):
        return self.name
