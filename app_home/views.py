import datetime
import random
import pytz
from django.contrib.auth.hashers import make_password, check_password
import re
from app_home import models, forms
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProManSaas.settings'


# 发送验证码
def send_proman_email(to_email, code):
    send_mail(
        '来自ProManSaas的验证',
        '您的验证码为：' + code,
        'mornibear@sina.com',
        [to_email],
    )


# 邮箱验证
def email(request):
    message = '404'
    match_email = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if request.method == 'POST':
        e_mail = request.POST['email']
        # 验证是否重复
        if models.User.objects.filter(email=e_mail):
            message = 'repeat'
        elif e_mail == '' or e_mail is None or not re.match(match_email, e_mail):
            message = 'check'
        else:
            # 是否为已发验证码并未注册
            if models.EmailCheck.objects.filter(email=e_mail):
                email_check = models.EmailCheck.objects.get(email=e_mail)
                c_time = email_check.c_time
                now = datetime.datetime.now()
                now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
                c_time = c_time.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
                # 验证是否时隔60s
                if (now - c_time).seconds < 60:
                    message = 'short'
                else:
                    random_number = str(random.randint(100000, 999999))
                    e_mail = email_check.email
                    email_check.code = random_number
                    email_check.c_time = datetime.datetime.now()
                    email_check.save()
                    send_proman_email(e_mail, random_number)
                    message = random_number
            else:
                # 将验证码和邮箱保存到数据库
                random_number = str(random.randint(100000, 999999))
                new_email_check = models.EmailCheck()
                new_email_check.email = e_mail
                new_email_check.code = random_number
                new_email_check.save()
                send_proman_email(e_mail, random_number)
                message = random_number

    return HttpResponse(message)


# 主页
def home(request):
    if request.session.get('is_login', None):
        user = models.User.objects.get(id=request.session.get('user_id'))
        request.session['user_name'] = user.name
        request.session['head_icon'] = user.head_icon.url
        request.session['notice'] = user.notice
        request.session['un_answer'] = user.un_answer
        request.session['answer_notice'] = user.answer_notice
        request.session['new_mission'] = user.new_mission
        request.session['deadline'] = user.deadline
    return render(request, 'app_home/home.html', locals())


# 登录
def login(request):
    if request.session.get('is_login', None):
        return redirect("home")
    if request.method == 'GET':
        login_form = forms.UserForm()
        return render(request, 'app_home/login.html', locals())
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        error_email = "请检查填写的邮箱！"
        error_password = "请检查填写密码！"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                # if check_password(password, user.password):
                if password == user.password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['head_icon'] = user.head_icon.url
                    request.session['notice'] = user.notice
                    request.session['un_answer'] = user.un_answer
                    request.session['answer_notice'] = user.answer_notice
                    request.session['new_mission'] = user.new_mission
                    request.session['deadline'] = user.deadline
                    return redirect('home')
                else:
                    error_email = None
                    error_password = "密码不正确！"
            except:
                error_email = "用户不存在！"
                error_password = None
        return render(request, 'app_home/login.html', locals())


# 注册
def register(request):
    # 登录状态不允许注册
    if request.session.get('is_login', None):
        return redirect("home")
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        error_name = "请检查填写内容"
        # error_email = "请检查填写内容"
        # error_password = "请检查填写内容"
        print(register_form.errors)
        if register_form.is_valid():
            # 获取数据

            name = register_form.cleaned_data['name']
            e_mail = register_form.cleaned_data['email']
            code = register_form.cleaned_data['code']
            password = register_form.cleaned_data['password']
            password_confirm = register_form.cleaned_data['password_confirm']

            email_check = models.EmailCheck.objects.get(email=e_mail)
            head_icon = "/static/image/user.png"
            true_name = name
            if password != password_confirm:  # 判断两次密码是否相同
                error_password = "两次输入的密码不同！"
                return render(request, 'app_home/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=name)
                if same_name_user:  # 用户名唯一
                    error_name = '用户已经存在'
                    return render(request, 'app_home/register.html', locals())
                same_email_user = models.User.objects.filter(email=e_mail)
                if same_email_user:  # 邮箱地址唯一
                    error_email = '该邮箱地址已被注册'
                    return render(request, 'app_home/register.html', locals())

                if code != email_check.code:
                    error_email = '验证码错误'
                    return render(request, 'app_home/register.html', locals())

            email_check.delete()
            new_user = models.User()
            new_user.name = name
            # new_user.password = make_password(password)
            new_user.password = password
            new_user.email = e_mail
            new_user.true_name = true_name
            new_user.head_icon = head_icon
            new_user.save()
            models.User.objects.filter(email=e_mail)
            return redirect('login')
    register_form = forms.RegisterForm()
    return render(request, 'app_home/register.html', locals())


# 注销
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("home")
    request.session.flush()
    return redirect("home")
