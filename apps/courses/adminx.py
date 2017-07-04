from .models import *
from organization.models import CourseOrg
import xadmin

# 添加课程的时候可以顺便添加章节
class LessonInline:
    model = Lesson
    extra = 0


# 添加课程的时候可以顺便添加课程资源
class CourseResourceInline:
    model = CourseResource
    extra = 0



class CourseAdmin(object):
    list_display=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_zj_nums']
    search_fields=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']

    model_icon = 'fa fa-graduation-cap'
    ordering = ['-click_nums']
    style_fields={"detail":"ueditor"}
    readonly_fields = ['click_nums']
    readonly_fields = ['fav_nums']

    list_editable = ['degree','desc']

    inlines = [LessonInline, CourseResourceInline]
    import_excel = True


    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


    def save_models(self):
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()





class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter = ['course__name','name','add_time']
    model_icon = 'fa fa-paper-plane-o'


class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter = ['lesson','name','add_time']
    model_icon = 'fa fa-file-video-o'


class CourseResourceAdmin(object):
    list_display=['course','name','download','add_time']
    search_fields=['course','name','download']
    list_filter = ['course','name','download','add_time']
    model_icon = 'fa fa-book'



class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']
    model_icon='fa fa-superpowers'

    ordering = ['-click_nums']

    readonly_fields = ['click_nums']
    readonly_fields = ['fav_nums']

    # Inline # 添加课程的时候可以顺便添加章节、课程资源
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)