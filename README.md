EduOnline在线教育


打造在线学习平台
兼容在python3.5下xadmin的使用
Django使用sina邮箱/163邮箱发送邮箱配置
使用Celery+Redis完成异步注册发送邮件功能
在Centos7下使用nginx+uwsgi部署该项目应用（本项目在windows系统环境下完成开发）
如果该项目对您学习或工作有帮助，欢迎start


开发环境
在windows系统下配置python3.5环境
Django1.10.5
Xadmin 0.6


项目功能




部署项目（linux）
克隆项目
git clone https://github.com/wocswang/Eduonline

配置项目环境
安装配置python3.5，mysql5.7,redis，nginx
进入到Mxonline目录中查找requirements.txt执行pip install -r requirements.txt,
等待项目的依赖。

配置数据库
确认你自己的数据库配置安装成功
在项目中的setting.py中DATABASES配置数据库信息

#这是我的数据库配置信息，可以作为参考
DATABASES ={
‘default’:{
‘ENGINE’ :  ‘django.db.backends.mysql’,
‘NAME’ : ’eduonline’,
‘USER’ : ‘root’,
‘PASSWORD : ‘123456’,
‘HOST’: ‘127.0.0.1’. 

}

}

导入数据
首先需要在你的数据库中创建一个库，这里我命名eduonline，并赋予权限。
这里我使用Navicat（任何数据库工具都可以）工具从开发环境的数据库中把数据导入	到linux服务器中的数据库。
使用makemigrations migrate命令创建数据表

配置redis
首先安装redis然后查看是否正常启动
在项目的setting.py中配置
#配置Broker
BROKER_URL = ‘redis://127.0.0.1:6379/0’
RROKER_TRANSPORT = ‘redis’	
配置完成后进入Eduonline目录中运行：
Celery -A demo workr -l debug
以此来测试celery的worker服务是否正常启动

配置nginx+uwsgi
1安装uwsgi
pip install uwsgi
2测试uwsgi
uwsgi --http:8000 --module Eduonline.wsgi

3配置nginx
1安装nginx(这里可以多中安装nginx方法就不一一介绍了，我这里用yum安装的)
2然后测试nginx是否正常运行启动。
3新建一个uc_nginx.conf文件（配置内容我已经放到项目conf目录中了）
4然后可以使用软连接ln -s 你的目录/Mxonline/conf/nginx/uc_nginx.conf/ /etc/nginx/conf.d/。当然也可以直接把uc_nginx.conf文件拷贝到/etc/nginx/conf.d下。

5需要拉取所有的static file文件到同一个目录下，所以在项目的setting.py文件中添加一行内容:
	STATIC_ROOT = os.path.join(BASE_DIR, "static/")
6运行命令：python manage.py collectstatic
7重启nginx

4配置uwsgi
这里我们通过配置文件启动uwsgi
1在项目Eduonline/conf目录下新建uwsgi.ini配置文件(配置内容我已经放到	conf/uwsgi.ini文件中了可供参考)
2配置成功后执行uwsgi -i 你的目录/Eduonline/conf/uwsgi.ini &

5访问
http://你的ip地址/

注释
1在项目上线时setting.py文件中必须设置的DEBUG=False
2本项目也可在python2.7中开发，需要把model.py中 def __str__(self):修改为def __unicode__(self):
3在setttings.py中django.coretext_processors修改为django.template.context_processors
4.目前xadmin不支持django1.11
5.在安装项目依赖DjangoUeditor3时如果安装失败
可以pip install git+https://github.com/twz915/DjangoUeditor3
