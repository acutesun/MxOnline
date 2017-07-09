from random import choice

from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http import  HttpResponse

from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.commons import is_user_login
from opreation.models import  UserFavorite


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')  # 默认按最新添加时间排序
        sort = request.GET.get('sort', '')  # 获取get方法传递的sort参数
        if sort:
            all_courses = Course.objects.all().order_by('-' + sort)  # 按照传递的参数降序排序
        popular = Course.objects.all().order_by('-click_nums')[:3]   # 热门课程

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        context = {
            'courses': courses,
            'sort': sort,
            'popular': popular,
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    def get(self, request, course_id):

        course = Course.objects.get(id=course_id)
        course.click_nums += 1  # 每次请求课程点击数量加1
        course.save()
        # 判断用户是否已经收藏课程和机构
        is_fav_course = False
        is_fav_org = False
        if is_user_login(request):
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                is_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                is_fav_org = True

        recommend = Course.objects.filter(category__exact=course.category).filter(~Q(id=course_id))   # 推荐类型相同相关课程
        if recommend:
            recommend = choice(list(recommend))
        context = {
            'course': course,
            'recommend': recommend,
            'is_fav_course': is_fav_course,
            'is_fav_org': is_fav_org,
        }
        return render(request, 'course-detail.html', context)


class CourseVideoView(View):

    def get(self, request):
        return render(request, 'course-video.html')