from django.conf.urls import url

from .views import OrgListView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

urlpatterns = [
    url(r'^list/', OrgListView.as_view(), name='orglist'),
    url(r'^userAsk/$', UserAskView.as_view(), name='userAsk'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    url(r'^add_fav/', AddFavView.as_view(), name='add_fav')
]
