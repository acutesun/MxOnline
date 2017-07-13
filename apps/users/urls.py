from django.conf.urls import url
from .views import UserInfoView, UserHeadImageView, UserAlterPwdView, UserCourseView, UserMsgView
from .views import UserFavOrgView, UserFavCourseView, UserFavTeacherView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),

    url(r'^alter_head/$', UserHeadImageView.as_view(), name='alter_head'),
    url(r'^alter_pwd/$', UserAlterPwdView.as_view(), name='alter_pwd'),
    url(r'^message/$', UserMsgView.as_view(), name='message'),

    url(r'^course/$', UserCourseView.as_view(), name='course'),

    url(r'^fav/org/$', UserFavOrgView.as_view(), name='fav_org'),
    url(r'^fav/teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    url(r'^fav/course/$', UserFavCourseView.as_view(), name='fav_course'),
]