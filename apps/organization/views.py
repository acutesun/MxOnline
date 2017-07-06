from django.shortcuts import render
from django.views import View
from organization.models import CityDict, CourseOrg


class OrgList(View):
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


