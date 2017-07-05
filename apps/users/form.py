from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)   # 这里的字段username要和前端的key相同
    password = forms.CharField(required=True, min_length=3)  # 不能为空并且长度不能小于3


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


