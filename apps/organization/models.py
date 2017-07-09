from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    name = models.CharField(max_length=50, verbose_name='机构名称')
    category = models.CharField(max_length=20, verbose_name='机构类别', default='pxjg',
                                choices=(('pxjg', '培训机构'), ('personal', '个人'), ('school', '学校')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图片', max_length=100)
    addr = models.CharField(max_length=150, verbose_name='机构地址')
    desc = models.CharField(max_length=200, verbose_name='机构描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teachers(self):
        ''' 返回该机构教师数量 '''
        return self.teacher_set.all().count()

    def get_courses(self):
        ''' 返回该机构课程数量 '''
        return self.course_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=20, verbose_name='教师名称')
    image = models.ImageField(max_length=100, upload_to='teacher/%Y/%m', verbose_name='教师头像', default=None, blank=True)
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='工作职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


