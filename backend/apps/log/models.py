from django.db import models


# Create your models here.
class Log(models.Model):
    api_name = models.CharField(verbose_name="接口名", max_length=200)
    method = models.CharField(verbose_name="请求方法", max_length=20)
    params = models.TextField(verbose_name="请求参数", max_length=5000, null=True, blank=True)
    comments = models.CharField(verbose_name="备注", max_length=255, null=True, blank=True)
    time = models.IntegerField(verbose_name="执行时长(毫秒)")
    ip = models.CharField(verbose_name="IP地址", max_length=64)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    username = models.CharField(verbose_name="访问用户", max_length=30)
    status_code = models.CharField(verbose_name="状态码", max_length=10)
    status_text = models.CharField(verbose_name="状态说明", max_length=30)

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.api_name
