from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import json
from django.core.urlresolvers import reverse

from .models import UserProfile, Banner
from opreation.models import UserCourse
from .form import LoginForm, RegisterForm, UserHeadImageForm, ModifyPwdForm
from utils.mixin_util import LoginRequiredMixin
from courses.models import Course
from opreation.models import UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher


# 4.自定义验证方法，修改邮箱用户名登录，默认只能用户名登录。
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if request.user.is_authenticated():
            return render(request, 'usercenter-info.html')
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
                return HttpResponseRedirect(reverse('index'))

            else:  # 验证失败还是回到登录界面
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})

        else:  # 验证输入格式不合法提示用户
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 将上一次的错误信息传递过来
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': '账户已存在'})
            password = request.POST.get('password', '')
            user = UserProfile()
            user.email = email
            user.username = email
            user.password = make_password(password)  # 对密码进行加密存入数据库
            user.save()
            request.user = user
            return redirect('index')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class UserInfoView(LoginRequiredMixin, View):
    ''' 用户中心 '''

    def get(self, request):
        return render(request, 'usercenter-info.html')


class UserCourseView(LoginRequiredMixin, View):
    ''' 用户所有课程 '''

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        course_ids = [user_course.course.id for user_course in user_courses]
        courses = Course.objects.filter(id__in=course_ids)
        context = {
            'courses': courses,
        }
        return render(request, 'usercenter-mycourse.html', context)


class UserFavOrgView(LoginRequiredMixin, View):
    ''' 用户收藏机构 '''

    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user).filter(fav_type=2)
        org_ids = [user_fav.fav_id for user_fav in user_favs]  # 课程机构的id
        orgs = CourseOrg.objects.filter(id__in=org_ids)
        context = {
            'orgs': orgs,
        }
        return render(request, 'usercenter-fav-org.html', context)


class UserFavTeacherView(LoginRequiredMixin, View):
    ''' 用户收藏讲师 '''

    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user).filter(fav_type=3)
        teacher_ids = [user_fav.fav_id for user_fav in user_favs]  # 收藏讲师的id
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        context = {
            'teachers': teachers,
        }
        return render(request, 'usercenter-fav-teacher.html', context)


class UserFavCourseView(LoginRequiredMixin, View):
    ''' 用户收藏课程 '''

    def get(self, request):
        user_favs = UserFavorite.objects.filter(user=request.user).filter(fav_type=1)
        courses_ids = [user_fav.fav_id for user_fav in user_favs]  # 收藏讲师的id
        courses = Course.objects.filter(id__in=courses_ids)
        context = {
            'courses': courses,
        }
        return render(request, 'usercenter-fav-course.html', context)


class UserMsgView(LoginRequiredMixin, View):
    ''' 用户消息 '''

    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user)
        unread_messages = UserMessage.objects.filter(user=request.user, has_read=False)
        for message in unread_messages:   # 设置为已阅读
            message.has_read = True
            message.save()
        context = {
            'messages': messages,
        }
        return render(request, 'usercenter-message.html', context)


class UserHeadImageView(LoginRequiredMixin, View):
    ''' 修改用户头像 '''

    def post(self, request):
        image_form = UserHeadImageForm(request.POST, request.FILES, instance=request.user)  # 将实例对象传入
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']  # 通过验证的图片会放在clean_data这个字典中去
            # request.user.image = image
            request.user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        return HttpResponse('{"status": "fail"}', content_type='application/json')


class UserAlterPwdView(LoginRequiredMixin, View):
    ''' 修改用户密码 '''

    def post(self, request):
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return HttpResponse('{"status": "fail", "msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(password2)
            request.user.save()
            return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(form.errors), content_type='application/json')


class IndexView(View):
    ''' 主页面 '''
    def get(self, request):
        banners = Banner.objects.order_by('-add_time')[:5]
        banner_courses = Course.objects.order_by('-add_time')[:3]
        courses = Course.objects.all()[:6]
        orgs = CourseOrg.objects.all()[:10]
        context = {
            'banners': banners,
            'banner_courses': banner_courses,
            'courses': courses,
            'orgs': orgs,
        }
        return render(request, 'index.html', context)


def page_not_found(request):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def page_errors(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response