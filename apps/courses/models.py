from datetime import datetime
from random import sample
from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name='课程教师', null=True, blank=True)
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程所属机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(choices=(('primary', '初级'), ('mid_level', '中级'),
                                       ('hig_level', '高级')), verbose_name='课程难度', max_length=200)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图片', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='back', choices=(('front', '前端'), ('database', '数据库'),
                                       ('back', '后端')), verbose_name='课程类别', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    prompt= models.CharField(max_length=200, default='', verbose_name='课程须知')
    learns = models.CharField(max_length=200, default='', verbose_name='你能学到什么')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lessons(self):
        return self.lesson_set.all().count()  # 返回课程章节数

    def get_user_course(self):  # 随机获取一个学习用户
        users = self.usercourse_set.all()
        if not users:
            users = []
        return users[:5]

    def get_all_lesson(self):
        ''' 获取所有的章节 '''
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=50, verbose_name='视频名')
    url = models.CharField(default='', max_length=200, verbose_name='课程地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name