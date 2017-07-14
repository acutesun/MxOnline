"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, LogoutView
from django.views.static import serve
from .settings import MEDIA_ROOT, STATIC_ROOT
from organization.views import TeacherListView, TeacherDetailView
urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),

    # 机构列表处理url
    url(r'^org/', include('organization.urls', namespace='org')),

    #  配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 公开课
    url(r'course/', include('courses.urls', namespace='course')),

    # 授课讲师
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),

    # 个人中心
    url(r'^user/', include('users.urls', namespace='user')),

    # settings中DEBUG设置为False， 静态文件路径失效。需要自己配置路径
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
