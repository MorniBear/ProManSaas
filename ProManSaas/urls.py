"""ProManSaas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_home import views as home_views
from app_process import views as process_views

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台管理
    path('', home_views.home, name='home'),  # home page
    path('login/', home_views.login, name='login'),  # 登录
    path('register/', home_views.register, name='register'),  # 注册
    path('logout/', home_views.logout, name='logout'),  # 注销
    path('email/', home_views.email, name='email'),
    path('captcha/', include('captcha.urls')),  # 验证码

    path('start/', process_views.project_start, name='start'),
    path('addmember/', process_views.add_member, name='add_member'),
    path('projectlist', process_views.project_list, name='project_list'),
    path('addmission/', process_views.add_mission, name='add_mission'),

]
