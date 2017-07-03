import xadmin
from .models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class CourseOrgAdmin(object):

    list_display = ['name', 'desc','city', 'click_nums', 'fav_nums', 'addr' 'add_time']
    list_filter = ['name', 'desc','city', 'click_nums', 'fav_nums', 'addr' 'add_time']
    search_fields = ['name', 'desc','city', 'click_nums', 'fav_nums', 'addr']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'add_time']
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)