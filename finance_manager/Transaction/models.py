from django.db import models
from django.core.validators import MinValueValidator
from Category.models import Category
from User.models import User
from Family.models import Family


# Create your models here.
class Transaction(models.Model):
    TYPE_CHOICES = (
        ("income", "收入"),
        ("expense", "支出"),
    )
    PAYMENT_METHOD_CHOICES = (
        ("cash", "现金"),
        ("wechat", "微信支付"),
        ("alipay", "支付宝"),
        ("card", "银行卡"),
        ("other", "其他"),
    )

    transaction_id = models.AutoField(primary_key=True, verbose_name="交易ID")
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="金额",
    )
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, verbose_name="交易类型"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="支付方式"
    )
    date = models.DateTimeField(verbose_name="交易时间")
    remark = models.TextField(blank=True, verbose_name="备注")
    # 外键关联
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="分类"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "transaction"
        verbose_name = "交易"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["family", "type"]),
        ]

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.related_user.nickname} - {self.amount}"
