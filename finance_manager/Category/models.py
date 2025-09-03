from django.db import models
from Family.models import Family


# Create your models here.
class Category(models.Model):
    TYPE_CHOICES = (
        ("income", "收入"),
        ("expense", "支出"),
    )

    category_id = models.AutoField(primary_key=True, verbose_name="分类ID")
    name = models.CharField(max_length=100, verbose_name="分类名称")
    icon = models.CharField(max_length=50, blank=True, verbose_name="图标")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="类型")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父分类"
    )
    family = models.ForeignKey(
        Family, on_delete=models.CASCADE, verbose_name="所属家庭"
    )

    class Meta:
        db_table = "category"
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        # 同一家庭下，同一父分类下的分类名不能重复
        unique_together = ("name", "parent", "family")

    def __str__(self):
        return f"{self.name} - {self.family.family_name}"
