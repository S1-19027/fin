from django.db import models
from Transaction.models import Transaction
from Tag.models import Tag


# Create your models here.
class TransactionTag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, verbose_name="交易"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="标签")

    class Meta:
        db_table = "transaction_tag"
        verbose_name = "交易标签关联"
        verbose_name_plural = verbose_name
        unique_together = ("transaction", "tag")  # 防止重复打标

    def __str__(self):
        return f"{self.transaction} - {self.tag}"
