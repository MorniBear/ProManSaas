from datetime import time

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from app_home import models
from app_process import forms


def add_mission(request):
    # 非登录状态下不允许邀请成员
    if not request.session.get('is_login', None):
        return redirect("login")
    # 非项目下访问不允许邀请成员
    if not request.session.get('has_project', None):
        return redirect('project_list')
    if request.method == 'GET':
        mission_form = forms.MissionFrom()

        project = models.Project.objects.get(id=request.session.get('project_id'))

        user = project.projectmember_set.get(user_id=request.session.get('user_id'))
        # 获取项目的所有任务
        mission = project.projectmission_set.all()

        power = user.get_member_power_display()
    if request.method == 'POST':
        pass
    return render(request, 'app_process/addmission.html', locals())


def add_member(request):
    # 非登录状态下不允许邀请成员
    if not request.session.get('is_login', None):
        return redirect("login")
    # 非项目下访问不允许邀请成员
    if not request.session.get('has_project', None):
        return redirect('project_list')
    # GET
    if request.method == 'GET':
        member_form = forms.MemberFrom()

        project = models.Project.objects.get(id=request.session.get('project_id'))

        user = project.projectmember_set.get(user_id=request.session.get('user_id'))
        # 获取项目所有成员
        members = project.projectmember_set.all()

        power = user.get_member_power_display()

    if request.method == 'POST':
        project = models.Project.objects.get(id=request.session.get('project_id'))
        member_form = forms.MemberFrom(request.POST)
        if member_form.is_valid():
            username = member_form.cleaned_data['user_name']
            user_power = member_form.cleaned_data['user_power']
            if models.User.objects.filter(name=username):
                if not project.projectmember_set.filter(user_name=username):
                    user = models.User.objects.get(name=username)
                    project_new_member = models.ProjectMember()
                    project_new_member.user_id = user.id
                    project_new_member.user_name = user.name
                    project_new_member.project_id = project.id
                    project_new_member.project_name = project.name
                    project_new_member.member_power = user_power
                    project_new_member.member_cost = 0
                    project_new_member.save()
                    return redirect('add_member')
        else:
            username = request.POST['name']
            if username == '':
                message = 'none'
            elif not models.User.objects.filter(name=username):
                message = 'notexist'
            elif project.projectmember_set.filter(user_name=username):
                message = 'has'
            else:
                message = 'ok'
            return HttpResponse(message)

    return render(request, 'app_process/addmember.html', locals())


def project_list(request):
    # 非登录状态下没有项目
    if not request.session.get('is_login', None):
        return redirect("login")
    # 获取当前登录账号的所有项目
    user = models.User.objects.get(id=request.session.get('user_id'))
    projects = user.project_set.all()

    return render(request, 'app_process/projectlist.html', locals())


def project_start(request):
    # 非登录状态下不允许创建项目
    if not request.session.get('is_login', None):
        return redirect("login")
    # get请求返回表单
    if request.method == 'GET':
        project_form = forms.StartFrom()
        return render(request, 'app_process/start.html', locals())
    # post请求接受信息
    if request.method == 'POST':
        project_form = forms.StartFrom(request.POST)
        message = "请检查填写信息"
        # 检测表单是否填了
        if project_form.is_valid():

            # 获取表单数据
            project_name = project_form.cleaned_data['project_name']
            project_state = project_form.cleaned_data['project_state']
            start_time = project_form.cleaned_data['start_time']
            pre_end_time = project_form.cleaned_data['pre_end_time']
            end_time = pre_end_time
            project_state = project_form.cleaned_data['project_state']
            project_description = project_form.cleaned_data['project_description']

            # 从session中获取数据
            user_id = request.session.get('user_id')
            user_name = request.session.get('user_name')
            # 默认上班时间为早上八点
            job_start = time(8, 0, 0)
            # 监测项目名是否重复
            if models.Project.objects.filter(name=project_name):
                message = "项目名重复"
                return render(request, 'app_process/start.html', locals())
            else:
                # 创建新的项目表数据项 包括
                # WorkDays
                # QuestionStatus
                # QuestionType
                # ProjectMember

                new_project = models.Project()
                new_project.name = project_name
                new_project.start_time = start_time
                new_project.pre_end_time = pre_end_time
                new_project.end_time = end_time
                new_project.status = project_state
                new_project.describe = project_description
                new_project.job_start = job_start
                new_project.user_name = user_name
                new_project.user_id = user_id
                new_project.save()
                this_id = new_project.id
                work_days = models.WorkDays()
                work_days.project_id = this_id
                work_days.value_time = pre_end_time
                work_days.save()

                question_status1 = models.QuestionStatus()
                question_status2 = models.QuestionStatus()
                question_status3 = models.QuestionStatus()
                question_status1.project_id = this_id
                question_status2.project_id = this_id
                question_status3.project_id = this_id
                question_status1.status = "待解决"
                question_status2.status = "已解决"
                question_status3.status = "追问中"
                question_status1.project_name = project_name
                question_status2.project_name = project_name
                question_status3.project_name = project_name
                question_status1.save()
                question_status2.save()
                question_status3.save()

                question_type1 = models.QuestionType()
                question_type2 = models.QuestionType()
                question_type3 = models.QuestionType()
                question_type1.project_id = this_id
                question_type2.project_id = this_id
                question_type3.project_id = this_id
                question_type1.type = "代码问题"
                question_type2.type = "工作问题"
                question_type3.type = "项目问题"
                question_type1.project_name = project_name
                question_type2.project_name = project_name
                question_type3.project_name = project_name
                question_type1.save()
                question_type2.save()
                question_type3.save()

                project_master = models.ProjectMember()
                project_master.user_id = user_id
                project_master.user_name = user_name
                project_master.project_id = this_id
                project_master.project_name = project_name
                project_master.member_power = 2
                project_master.member_cost = 0
                request.session['has_project'] = True
                request.session['project_id'] = this_id
                request.session['project_name'] = project_name
                project_master.save()
                return redirect('add_member')
    return render(request, 'app_process/start.html', locals())
