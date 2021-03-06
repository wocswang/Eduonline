# _*_ encoding: utf-8 _*_
import json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile,EmailVertifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCousre,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from users.models import Banner

from .task import send_register_email

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LogoutView(View):
    #用户登出
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse("index"))



class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVertifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html" )


class UserInfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


#个人中心修改密码
class UpdatePwdView(LoginRequiredMixin,View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

#发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}',content_type='application/json')
        send_register_email(email,"update_email")
        return HttpResponse('{"email":"success"}', content_type='application/json')


#修改个人邮箱
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVertifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user=request.user
            user.email =email
            user.save()
            return HttpResponse('{"email":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

#我的课程
class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_courses =UserCousre.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses":user_courses
        })

#我的收藏
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list =[]
        fav_orgs =UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org =CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list":org_list
        })

class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list
        })

#我的消息
class MymessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        #对个人消息分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages,5, request=request)

        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            "messages":messages

        })


class IndexView(View):
    #皎月网 首页
    def get(self,request):
        #取出轮播图
        all_banners=Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses =Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html',{
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses": banner_courses,
            "course_orgs":course_orgs

        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code=404
    return response

# 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(username=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            register_user = UserProfile()
            register_user.username = user_name
            register_user.email = user_name
            register_user.password = make_password(pass_word)
            register_user.is_active = False
            register_user.save()

            #写入欢迎注册消息
            register_message = UserMessage()
            register_message.user=register_user.id
            register_message.message="欢迎注册皎月网"
            register_message.save()





            send_register_email(user_name,"register")
            return  render(request,"login.html")
        else:
            return render(request, "register.html",{"register.html":register_form})
        #     send_em = send_email(email, "register")
        #     if send_em:
        #         return render(request, "login.html", )
        # else:
        #     email = request.POST.get("email", "")
        #     password = request.POST.get("password", "")
        #     return render(request, "register.html",
        #               {"register_form": register_form, "email": email, "password": password})

class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request, "send_success.html")

class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVertifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html",{"email":email} )
        else:
            return render(request, "active_fail.html" )
        return render(request, "login.html" )


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email","")
            if pwd1 !=pwd2:
                return render(request, "password_reset.html", {"email":email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request,"login.html")
        else:
            email = request.POST.get("email","")
            return render(request, "password_reset.html", {"email": email})

def index(request):
    send_register_email.delay()
    return HttpResponse(u"邮件发送成功， 请查收")

# def user_login(request):
#     if request.method=="POST":
#         user_name=request.POST.get("username","")
#         pass_word=request.POST.get("password","")
#         user=authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html",{})
#         else:
#             return render(request, "login.html", {"msg":"用户名或者密码错误！"})
#     elif request.method=="GET":
#         return render(request,"login.html",{})