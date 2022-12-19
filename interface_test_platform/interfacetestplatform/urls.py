__author__ = '蒋运生'
from . import views
from django.urls import path, include
from django.conf import settings
from django.urls import re_path
from django.views import static

# if settings.DEBUG==False:
#     urlpatterns += [
#         re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
#     ]


urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('project/', views.project, name="project"),
    path('module/', views.module, name="module"),
    path('test_case/', views.test_case, name="test_case"),
    path('case_suite/', views.case_suite, name="case_suite"),
    re_path('test_case_detail/(?P<test_case_id>[0-9]+)', views.test_case_detail, name="test_case_detail"),
    re_path('module_test_cases/(?P<module_id>[0-9]+)', views.module_test_cases, name="module_test_cases"),
    re_path('add_case_in_suite/(?P<suite_id>[0-9]+)', views.add_case_in_suite, name="add_case_in_suite"),
]
