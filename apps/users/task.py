# _*_ encoding:utf-8 _*_
from Eduonline.celery import app
import random

from .models import EmailVertifyRecord
from django.core.mail import send_mail

from Eduonline.settings import EMAIL_FROM


def random_str(lens):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chars_len=len(chars)-1
    for i in range(lens):
        str+=chars[random.randint(0,chars_len)]
    return str

@app.task
def send_register_email(email, send_type="register"):
    email_record = EmailVertifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "皎月在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://www.imooc.com/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "皎月在线网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://www.imooc.com/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "皎月在线邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass