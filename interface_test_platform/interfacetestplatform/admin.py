from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project_owner", "test_owner", "dev_owner", "desc", "create_time", "update_time")

admin.site.register(models.Project, ProjectAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "name","belong_project", "test_owner", "desc", "create_time", "update_time")

admin.site.register(models.Module, ModuleAdmin)

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "case_name","belong_project", "belong_module", "request_data", "uri", "assert_key", "creator", "extract_var", "request_method",
                    "status", "create_time", "update_time", "user")
admin.site.register(models.TestCase, TestCaseAdmin)

class CaseSuiteAdmin(admin.ModelAdmin):
    list_display = ("id", "suite_desc", "creator", "creator_time")

admin.site.register(models.CaseSuite, CaseSuiteAdmin)