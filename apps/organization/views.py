from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from organization.models import CityDict, CourseOrg
from opreation.models import UserFavorite
from .forms import UserAskForm
from utils.commons import is_user_login


class OrgListView(View):  # 处理课程机构列表展示
    def get(self, request):
        all_city = CityDict.objects.all()
        all_org = CourseOrg.objects.all()
        org_nums = all_org.count()   # 课程机构数量
        context = {
            'all_city': all_city,
            'all_org': all_org,
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
        is_fav = has_fav(request, org.id)  # 判断是否已经收藏机构
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
        is_fav = has_fav(request, org.id)  # 判断是否已经收藏机构
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
        is_fav = has_fav(request, org.id)  # 判断是否已经收藏机构
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
        is_fav = has_fav(request, org.id)  # 判断是否已经收藏机构
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

        # 查询是否已经收藏
        records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if records:  # 如果存在再次点击取消收藏
            records.delete()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:        # 不存在则收藏并保存到数据库
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')


def has_fav(request, org_id):
    ''' 判断用户是否已经收藏机构 '''
    fav = UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2)
    if is_user_login(request) and fav:
        return True
    return False