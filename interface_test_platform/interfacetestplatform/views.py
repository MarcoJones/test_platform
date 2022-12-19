from django.shortcuts import render, redirect
from django.contrib import auth
from .form import UserForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import traceback
from .models import Project, Module, TestCase, CaseSuite, SuiteCase
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage


@login_required
def index(request):
    """
    首页视图函数
    :param request:
    :return:
    """
    return  render(request, 'index.html')

def login(request):
    """
    登录页视图函数
    :param request:
    :return:
    """
    print("request.session.items(): {}".format(request.session.items()))
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = u"请检查填写内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 使用django提供的身份验证功能
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    print("用户【%s】登录成功" % username)
                    auth.login(request, user)
                    request.session['is_login'] = True
                    # 登录成功跳转至主页
                    return redirect('/')
                else:
                    message = "用户名不存在或密码不正确！"
            except:
                traceback.print_exc()
                message = "登录失败，请稍后重试！"
        # 用户名或密码为空，返回登录页和错误提示信息
        else:
            return render(request, 'login.html', locals())
    # 不是表单提交，代表只是访问登录页
    else:
        login_form = UserForm()
        return render(request, 'login.html', locals())

def register(request):
    """
    注册视图函数
    :param request:
    :return:
    """
    return render(request, 'register.html')


@login_required
def logout(request):
    """
    登出视图函数
    :return:
    """
    auth.logout(request)
    request.session.flush()
    return redirect('/login/')

@login_required
def project(request):
    """
    项目管理页面视图
    :param request:
    :return:
    """
    print("request.user.is_authenticated:", request.user.is_authenticated)
    projects = Project.objects.filter().order_by('-id')
    print("project:", projects)
    return render(request, 'project.html', {'projects':get_paginator(request, projects)})

def get_paginator(request, data):
    """
    封装分页函数
    :param request:
    :param data:
    :return:
    """
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    try:
        paginator_pages = paginator.page(page)
    except PageNotAnInteger:
        paginator_pages = paginator.page(1)
    except InvalidPage:
        return HttpResponse('找不到页面内容')
    return paginator_pages

@login_required
def module(request):
    """
    模块视图函数
    :param request:
    :return:
    """
    if request.method == "GET":
        modules = Module.objects.filter().order_by('-id')
        return render(request, 'module.html', {'modules': get_paginator(request, modules)})
    else:
        project_name = request.POST['project_name']
        projects = Project.objects.filter(name__contains=project_name.strip())
        projs = [proj.id for proj in projects]
        modules = Module.objects.filter(belong_project__in=projs)
        return render(request, 'module.html', {'modules': get_paginator(request, modules), 'project_name': project_name})

@login_required
def test_case(request):
    """
    测试用例试图函数
    :param request:
    :return:
    """
    print("request.session['is_login']: {}".format(request.session['is_login']))
    test_cases = ""
    if request.method == "GET":
        test_cases = TestCase.objects.filter().order_by('id')
        print("testcase: {}".format(test_cases))
    elif request.method == "POST":
        print("request.POST: {}".format(request.POST))
        test_case_id_list = request.POST.getlist('testcase_list')
        if test_case_id_list:
            test_case_id_list.sort()
            print("test_case_id_list:{}".format(test_case_id_list))
        test_cases = TestCase.objects.filter().order_by("id")
    return render(request, "test_case.html", {'test_cases': get_paginator(request, test_cases)})

@login_required
def test_case_detail(request, test_case_id):
    """
    用例详情页视图函数
    :param request:
    :return:
    """
    test_case_id = int(test_case_id)
    test_case = TestCase.objects.get(id=test_case_id)
    print("test_case:{}".format(test_case))
    print("test_case.belong_project:{}".format(test_case.belong_project))
    return render(request, 'test_case_detail.html', {'test_case': test_case})

@login_required
def module_test_cases(request, module_id):
    module = ""
    if module_id:
        module = Module.objects.get(id = int(module_id))
        print(module)
    test_cases = TestCase.objects.filter(belong_module = module).order_by('-id')
    return render(request, 'test_case.html', {'test_cases': get_paginator(request, test_cases)})

@login_required
def case_suite(request):
    """
    用例集函数
    :param request:
    :return:
    """
    case_suites = CaseSuite.objects.filter()
    print("case_suite:{}".format(case_suites[0].suite_desc))
    return render(request, 'case_suite.html', {'case_suites': get_paginator(request, case_suites)})

@login_required
def add_case_in_suite(request, suite_id):
    """
    集合关联用例函数
    :param request:
    :return:
    """
    #查询指定的用例集合
    case_suite = CaseSuite.objects.get(id = suite_id)
    #根据用例ID查询所有用例
    test_case = TestCase.objects.filter().order_by('id')
    if request.method == 'GET':
        print("test_case:", test_case)

    elif request.method == 'POST':
        test_cases_list = request.POST.getlist('testcase_list')
        if test_cases_list:
            print("勾选的用例ID：", test_cases_list)
            for test_case in test_cases_list:
                case = TestCase.objects.get(id=int(test_case))
                SuiteCase.objects.create(case_suite=case_suite, test_case=case)
        else:
            print("添加用例失败！")
            return HttpResponse("添加的测试用例为空，请勾选用例后再添加！")
        return render(request, 'add_case_in_suite.html', {'test_case': get_paginator(request, test_case),
                                                          'case_suite': case_suite})