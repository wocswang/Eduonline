from .models import *
import xadmin

class CityDictAdmin(object):
    list_display=['name','desc','add_time']
    search_fields=['name','desc']
    list_filter=['name','desc','add_time']
    model_icon =  'fa fa-building-o'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','click_nums', 'fav_nums','image', 'address','city', 'add_time']
    search_fields = ['name', 'desc','click_nums', 'fav_nums','image', 'address','city']
    list_filter = ['name', 'desc','click_nums', 'fav_nums','image', 'address','city', 'add_time']
    model_icon = 'fa fa-sitemap'
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display=['org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    search_fields=['org','name','work_years','work_company','work_position','points','click_nums','fav_nums']
    list_filter=['org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    model_icon = 'fa fa-male'

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
