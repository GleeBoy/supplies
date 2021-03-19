from django.db import models
from django.contrib.auth.models import User
import os, logging

# Create your models here.


class Superclass(models.Model):
    code = models.CharField(verbose_name="编号", max_length=2)
    name = models.CharField(verbose_name="名字", max_length=32)
    description = models.CharField(verbose_name="描述", max_length=72, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'superclass'
        ordering = ['id']


class Subclass(models.Model):
    superclass = models.ForeignKey(Superclass, on_delete=models.CASCADE, verbose_name="父类", null=True)
    code = models.CharField(verbose_name="编号", max_length=2)
    name = models.CharField(verbose_name="名字", max_length=32)
    example = models.CharField(verbose_name="举例", max_length=72, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subclass'
        ordering = ['superclass', 'code']


# def request_user(instance):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return instance.user


class MaterialInfo(models.Model):
    item_code = models.CharField(verbose_name="中安料号", unique=True, max_length=20)
    item_name = models.CharField(verbose_name="类别", max_length=32)
    describe = models.CharField(verbose_name="描述", max_length=256, null=True)
    firm_code = models.CharField(verbose_name="厂商型号", max_length=20)    # 和厂商名字一样才算重复
    firm_name = models.CharField(verbose_name="厂商名字", max_length=32)
    material_img = models.ImageField(verbose_name="物料照片", upload_to='img', blank=True, null=True)
    specification = models.FileField(verbose_name="规格书", upload_to='specification', blank=True, null=True)
    remark = models.CharField(verbose_name="备注", max_length=256, null=True)
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="操作员")

    def delete(self, using=None, keep_parents=False):
        if self.material_img:
            try:
                os.remove(self.material_img.path)
            except Exception as e:
                logging.error(e)
        if self.specification:
            try:
                os.remove(self.specification.path)
            except Exception as e:
                logging.error(e)
        super(MaterialInfo, self).delete(using=None, keep_parents=False)

    class Meta:
        db_table = 'materialinfo'
        ordering = ['-id']
