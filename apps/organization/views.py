from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from organization.models import CityDict, CourseOrg
from .forms import UserAskForm


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
        context = {
            'org': org,
            'courses': courses,
            'teachers': teachers,
            'current_page': page,
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    ''' 机构所有课程 '''
    def get(self, request, org_id):
        page = 'course'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        courses = org.course_set.all()  # 通过机构对象获取所有的课程
        context = {
            'org': org,
            'courses': courses,
            'current_page': page,
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    ''' 机构介绍 '''
    def get(self, request, org_id):
        page = 'desc'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        courses = org.course_set.all()  # 通过机构对象获取所有的课程
        context = {
            'org': org,
            'current_page': page,
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    ''' 机构教师 '''
    def get(self, request, org_id):
        page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))  # 获取从机构列表点击过来的机构对象
        teachers = org.teacher_set.all()
        # 教师课程数量还没一实现
        context = {
            'org': org,
            'teachers': teachers,
            'current_page': page,
        }
        return render(request, 'org-detail-teachers.html', context)


