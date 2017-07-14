from random import choice

from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.http import  HttpResponse

from .models import Course, CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.commons import is_user_login
from opreation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_util import LoginRequiredMixin


class CourseListView(View):
    ''' 所有课程列表 '''
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')  # 默认按最新添加时间排序
        # 排序
        sort = request.GET.get('sort', '')  # 获取get方法传递的sort参数
        if sort:
            all_courses = Course.objects.all().order_by('-' + sort)  # 按照传递的参数降序排序
        popular = Course.objects.all().order_by('-click_nums')[:3]   # 热门课程
        # 检索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:   # 找出含有keywords的course对象
            all_courses = Course.objects.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        # 分页
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
    ''' 课程详情页面 '''
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


class CourseInfoView(LoginRequiredMixin, View):
    ''' 课程章节 '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(user=request.user)
        ids = [user_course.course.id for user_course in user_courses]  # 得到当前用户学习过的所有课程id
        learn_courses = Course.objects.filter(id__in=ids)[:2]   # 得到所有学习的课程
        resource = CourseResource.objects.filter(course=course)  # 下载资源
        context = {
            'course': course,
            'resource': resource,
            'learn_courses': learn_courses,
        }
        return render(request, 'course-video.html', context)


class CourseCommentView(View):
    ''' 课程评论页面 '''
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        resource = CourseResource.objects.filter(course=course)  # 下载资源
        user_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(user=request.user)
        ids = [user_course.course.id for user_course in user_courses]  # 得到当前用户学习过的所有课程id
        learn_courses = Course.objects.filter(id__in=ids)[:2]  # 得到所有学习的课程

        context = {
            'course': course,
            'resource': resource,
            'user_comments': user_comments,
            'learn_courses': learn_courses,
        }
        return render(request, 'course-comment.html', context)


class AddCommentView(View):
    ''' 添加课程评论 '''
    def post(self, request):

        if not is_user_login(request):
            # 判断用户登录
            return HttpResponse('{"status": "fail", "msg": "未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')

        flag = False
        if int(course_id) > 0 and comments:
            c_comments = CourseComments()
            c_comments.user = request.user
            c_comments.course = Course.objects.get(id=int(course_id))
            c_comments.comments = comments
            c_comments.save()
            flag = True

        msg, status = ('添加成功', 'success') if flag else ('添加失败', 'fail')
        # 注意这里“%s” 必须加双引号。因为里面也必须是字符串，不加双引号就变成了'{"status": success, "msg": 添加成功}'
        data = '{"status": "%s", "msg": "%s"}' % (status, msg)
        return HttpResponse(data, content_type='application/json')




