import xadmin
from .models import *


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums']


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    list_filter = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    list_filter = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'add_time']
    list_filter = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)


