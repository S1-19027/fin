from django.db import models

# Create your models here.
class OperationLog(models.Model):
    """操作日志模型"""
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', verbose_name="用户")
    operation_type = models.CharField(max_length=20, null=False, verbose_name="操作类型")
    operation_time = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")
    operation_content = models.CharField(max_length=200, verbose_name="操作内容")

    class Meta:
        db_table = 'operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'

    def __str__(self):
        return f"{self.user.nickname} - {self.operation_type}"