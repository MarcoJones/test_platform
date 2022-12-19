from django.db import models
from smart_selects.db_fields import GroupedForeignKey # 后台级联选择
from django.contrib.auth.models import User


# 项目表
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    project_owner = models.CharField('项目负责人', max_length=20, null=False)
    test_owner = models.CharField('测试负责人', max_length=20, null=False)
    dev_owner = models.CharField('开发负责人', max_length=20, null=False)
    desc = models.CharField('项目描述', max_length=120, null=True)
    create_time = models.DateTimeField('项目创建时间', auto_now_add=True)
    update_time = models.DateTimeField('项目更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目信息表'
        verbose_name_plural = '项目信息表'

# 模块表
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('模块名称', max_length=32, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    test_owner = models.CharField('测试负责人', max_length=32, null=False)
    desc = models.CharField('模块描述', max_length=156, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '模块信息表'
        verbose_name_plural = '模块信息表'

# 测试用例表
class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField('用例名称', max_length=50, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    belong_module = GroupedForeignKey(Module, "belong_project", on_delete=models.CASCADE, verbose_name='所属模块')
    request_data = models.CharField('请求数据', max_length=1024, null=False, default='')
    uri = models.CharField('接口地址', max_length=1024, null=False, default='')
    assert_key = models.CharField('断言内容', max_length=1024, null=True)
    creator = models.CharField('创建人', max_length=100, null=False, default='')
    extract_var = models.CharField('提取变量表达式', max_length=1024, null=True)
    request_method = models.CharField('请求方式', max_length=100, null=True)
    status = models.IntegerField('用例状态', help_text="0:表示有效；1：表示无效")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='责任人', null=True)

    def __str__(self):
        return self.case_name

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = '测试用例表'

# 用例集合表
class CaseSuite(models.Model):

    id = models.AutoField(primary_key = True)
    suite_desc = models.CharField('用例集合描述', max_length=100, blank=True, null=True)
    if_execute = models.IntegerField(verbose_name = "是否执行", null=False, default=0, help_text='0:执行,1:不执行')
    test_case_model = models.CharField("测试执行模式", max_length=100, blank=True, null=True, help_text='data/keyword')
    creator = models.CharField('创建者', max_length=50, blank=True, null=True)
    creator_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '用例集合表'
        verbose_name_plural = '用例集合表'

#用例集合关联表
class SuiteCase(models.Model):
    id = models.AutoField(primary_key=True)
    case_suite = models.ForeignKey(CaseSuite, on_delete=models.CASCADE, verbose_name='用例集合')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='测试用例')
    status = models.IntegerField(verbose_name = '是否有效', null = False, default=1, help_text='0:无效，1：有效')
    create_time = models.DateTimeField('创建时间', auto_now=True)


