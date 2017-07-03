import xadmin
from .models import EmailVerifyRecord, Banner

from xadmin import views


class BaseSetting(object):
    enable_themes = True   # 使用主题
    use_bootswatch = True  # 主题格式


class GlobalSettings(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'   # 将app下的模型类收起

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type']
    search_fields = ['code', 'email', 'send_type']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index']
    search_fields = ['title', 'image', 'url', 'index']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
