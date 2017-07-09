from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseVideoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^video/(?P<course_id>\d+)$', CourseVideoView.as_view(), name='course_video'),
]
