# _*_ encoding:utf-8 _*_

from .models import EmailVertifyRecord,Banner
from xadmin import views
import xadmin

class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GlobalSettings(object):
    site_title="皎月后台管理系统平台"
    site_footer = "皎月课堂"
    menu_style="accordion"

class EmailVertifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'add_time']
    search_fields = ['title']
    list_filter = ['title', 'add_time']
    model_icon = 'fa fa-user-circle-o'

xadmin.site.register(EmailVertifyRecord,EmailVertifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

