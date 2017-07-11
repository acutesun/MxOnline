from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from organization.models import CityDict, CourseOrg
from courses.models import Course
from opreation.models import UserFavorite
from .forms import UserAskForm
from utils.commons import is_user_login
from .models import Teacher


class OrgListView(View):  # 处理课程机构列表展示
    def get(self, request):
        all_city = CityDict.objects.all()
        all_org = CourseOrg.objects.all()
        org_nums = all_org.count()   # 课程机构数量

        # 检索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:  # 找出含有keywords的course对象
            all_org = CourseOrg.objects.filter(Q(name__icontains=search_keywords) |
                                               Q(desc__icontains=search_keywords))
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 3, request=request)
        all_orgs = p.page(page)

        context = {
            'all_city': all_city,
            'all_org': all_orgs,
            'org_nums': org_nums,
        }
        return render(request, 'org-list.html', context)


class UserAskView(View):   # 处理 课程列表左边的 用户咨询

    def post(self, request):
        ask_form = UserAskForm(request.POST)  # 使用自定义的 Form 验证post提交的数据
        if ask_form.is_valid():
            user_ask = ask_form.save(commit=True)  # 验证合法提交到数据库, 返回userask实例
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')


class OrgHomeView(View):
    ''' 机构首页 '''
    def get(self, request, org_id):
        page = 'home'
        org = CourseOrg.objects.get(id=int(org_id))   # 获取从机构列表点击过来的机构对象
        courses = org.course_set.all()  # 通过机构对象获取所有的课程
        teachers = org.teacher_set.all()  # 获取所有的老师
        is_fav = has_fav(request, org.id, 2)  # 判断是否已经收藏机构
        context = {
            'org': org,
            'courses': courses,
            'teachers': teachers,
            'current_page': page,
            'is_fav': is_fav,  # 机构是否收藏
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    ''' 机构所有课程 '''
    def get(self, request, org_id):
        page = 'course'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        courses = org.course_set.all()  # 通过机构对象获取所有的课程
        is_fav = has_fav(request, org.id, 2)  # 判断是否已经收藏机构
        context = {
            'org': org,
            'courses': courses,
            'current_page': page,
            'is_fav': is_fav,  # 机构是否收藏
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    ''' 机构介绍 '''
    def get(self, request, org_id):
        page = 'desc'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        courses = org.course_set.all()  # 通过机构对象获取所有的课程
        is_fav = has_fav(request, org.id, 2)  # 判断是否已经收藏机构
        context = {
            'org': org,
            'current_page': page,
            'is_fav': is_fav,  # 机构是否收藏
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    ''' 机构教师 '''
    def get(self, request, org_id):
        page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        teachers = org.teacher_set.all()
        is_fav = has_fav(request, org.id, 2)  # 判断是否已经收藏机构
        # 教师课程数量还没一实现
        context = {
            'org': org,
            'teachers': teachers,
            'current_page': page,
            'is_fav': is_fav,  # 机构是否收藏
        }
        return render(request, 'org-detail-teachers.html', context)


class AddFavView(View):
    ''' 课程机构 收藏 功能 '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not is_user_login(request):
            # 判断用户登录
            return HttpResponse('{"status": "fail", "msg": "未登录"}', content_type='application/json')

        # 查询是否已经收藏, 如果存在再次点击取消收藏
        records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if records:
            records.delete()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')

        # 不存在则收藏并保存到数据库
        user_fav = UserFavorite()
        flag = False
        if int(fav_id) > 0 and int(fav_type) > 0:
            user_fav.fav_id = fav_id
            user_fav.fav_type = fav_type
            user_fav.user = request.user
            user_fav.save()
            flag = True
        msg, status = ('已收藏', 'success') if flag else ('收藏失败', 'fail')
        return HttpResponse('{"status": "%s", "msg": "%s"}' % (status, msg), content_type='application/json')


def has_fav(request, id, type):
    ''' 判断用户是否已经收藏机构 课程 教师 '''
    if is_user_login(request):  # 必须先判断用户是否登录，否则request.user为空
        if UserFavorite.objects.filter(user=request.user, fav_id=id, fav_type=type):
            return True
    return False


class TeacherDetailView(View):
    ''' 讲师详情页面 '''
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher_courses = teacher.course_set.all()[:5]

        is_fav_org = has_fav(request, teacher.org.id, 2)  # 判断是否已经收藏机构
        is_fav_teacher = has_fav(request, teacher.id, 3)  # 判断是否已经收藏教师

        context = {
            'teacher': teacher,
            'teacher_courses': teacher_courses,
            'is_fav_org': is_fav_org,
            'is_fav_teacher': is_fav_teacher,
        }
        return render(request, 'teacher-detail.html', context)


class TeacherListView(View):
    ''' 所有讲师列表页 '''
    def get(self, request):
        teachers = Teacher.objects.all()
        # 排序
        sort = request.GET.get('sort', '')
        sort_teachers = teachers.order_by('-click_nums')  # 按照点击量排序
        if sort == 'hot':
            teachers = sort_teachers
        # 检索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:  # 找出含有keywords的teacher对象
            teachers = Teacher.objects.filter(Q(name__icontains=search_keywords))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, 2, request=request)
        page_teachers = p.page(page)

        context = {
            'teachers': teachers,
            'page_teachers': page_teachers,
            'sort_teachers': sort_teachers[:3],  # 取3个热门教师
            'sort': sort,
        }
        return render(request, 'teachers-list.html', context)