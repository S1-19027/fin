from django.db import models
from Transaction.models import Transaction
from User.models import User
# Create your models here.
class TransactionUsers(models.Model):
    """交易分摊模型"""
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, db_column='transaction_id', verbose_name="交易")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_id', verbose_name="用户")
    share_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="分摊金额")

    class Meta:
        db_table = 'transaction_splits'
        verbose_name = '交易分摊'
        verbose_name_plural = '交易分摊'

    def __str__(self):
        return f"{self.user.nickname} - {self.share_amount}"