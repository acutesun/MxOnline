from django.conf.urls import url
from .views import UserInfoView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),

]