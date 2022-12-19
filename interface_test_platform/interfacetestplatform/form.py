__author__ = '蒋运生'
from django import forms

# 用户登录表单
class UserForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=128, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    password = forms.CharField(label=u"密码", max_length=256, widget=forms.PasswordInput(attrs = {'class': 'form-control'}))