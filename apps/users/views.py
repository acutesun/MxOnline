from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile
from .form import LoginForm


# 4.自定义验证方法，修改邮箱用户名登录，默认只能用户名登录。
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 5.后台验证前端用户密码的输入格式
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 1.获取用户密码
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 2.验证用户密码
            user = authenticate(username=username, password=password)  # 返回一个UserProfile对象
            # 3. 验证成功跳转到主页或者个人中心
            if user is not None:
                login(request, user)
                return render(request, 'index.html')

            else:   # 验证失败还是回到登录界面
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})

        else:  # 验证输入格式不合法提示用户
            return render(request, 'login.html', {'login_form': login_form})











