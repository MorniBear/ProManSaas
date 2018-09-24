from django.db import models


# Create your models here.

# 用户表
class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)  # 用户名
    password = models.CharField(max_length=128)  # 密码
    true_name = models.CharField(max_length=128, verbose_name='真实姓名')
    email = models.EmailField(verbose_name='邮箱', unique=True)
    head_icon = models.ImageField(upload_to='', verbose_name='头像')  # 配置问题待讨论
    notice = models.PositiveIntegerField(verbose_name='通知数', default=0, auto_created=True)
    un_answer = models.PositiveIntegerField(verbose_name='未回答问题数', default=0, auto_created=True)
    answer_notice = models.PositiveIntegerField(verbose_name='回答通知数', default=0, auto_created=True)
    new_mission = models.PositiveIntegerField(verbose_name='新任务通知数', default=0, auto_created=True)
    deadline = models.PositiveIntegerField(verbose_name='即将到期通知数', default=0, auto_created=True)
    signature = models.TextField(verbose_name='个人简介', default='这个家伙很懒懒', auto_created=True)
    location = models.CharField(max_length=128, verbose_name='所在地', default='未知', auto_created=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


# 项目表
class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名')
    describe = models.TextField(verbose_name='项目描述', default='该项目暂无描述')
    user_id = models.ForeignKey('User', verbose_name='所属用户', on_delete=models.CASCADE)
    status = models.CharField(max_length=128, default="筹备状态", verbose_name="项目状态")
    process = models.PositiveIntegerField(verbose_name="项目进度", default=0, auto_created=True)
    all_mission_number = models.PositiveIntegerField(verbose_name="总任务数", default=0, auto_created=True)
    all_users_number = models.PositiveIntegerField(verbose_name="参与人数", default=0, auto_created=True)
    start_time = models.DateField(verbose_name="项目开始日期")
    pre_end_time = models.DateField(verbose_name="预计结束时间")
    end_time = models.DateField(verbose_name="实际结束时间", default=None, auto_created=True)
    job_start = models.TimeField(verbose_name='上班时间')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目"
        verbose_name_plural = "项目"


# 上班日期表
class WorkDays(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    monday = models.BooleanField(default=True, verbose_name='周一是否上班', auto_created=True)
    tuesday = models.BooleanField(default=True, verbose_name='周二是否上班', auto_created=True)
    wednesday = models.BooleanField(default=True, verbose_name='周三是否上班', auto_created=True)
    thursday = models.BooleanField(default=True, verbose_name='周四是否上班', auto_created=True)
    friday = models.BooleanField(default=True, verbose_name='周五是否上班', auto_created=True)
    saturday = models.BooleanField(default=True, verbose_name='周六是否上班', auto_created=False)
    sunday = models.BooleanField(default=True, verbose_name='周日是否上班', auto_created=False)
    value_time = models.DateField(auto_created=True, verbose_name="适用时间")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "都那些天上班"
        verbose_name_plural = "都那些天上班"


# 问题表
class Question(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=128, verbose_name="问题标题")
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    type = models.ForeignKey('QuestionType', on_delete=models.CASCADE, verbose_name='所属问题类型')
    status = models.ForeignKey('QuestionStatus', on_delete=models.CASCADE, verbose_name='所属问题状态')
    content = models.TextField(verbose_name='问题内容')
    answer_number = models.PositiveIntegerField(verbose_name='回答数')
    questioner_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='提问人')
    c_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    end_time = models.DateTimeField(auto_created=True, default=None, verbose_name="完成时间")
    new_question_id = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='追答问题id')

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "问题"
        verbose_name_plural = "问题"


class Answer(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='所属问题')
    question_title = models.CharField(max_length=128, verbose_name='问题标题')
    answer_text = models.TextField(verbose_name='回答内容')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "回答"
        verbose_name_plural = "回答"


class QuestionStatus(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    status = models.CharField(max_length=128, verbose_name='状态')
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    project_name = models.CharField(max_length=128, default=project_id.name, auto_created=True, verbose_name='项目名')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "问题状态"
        verbose_name_plural = "问题状态"


class QuestionType(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=128, verbose_name='类型')
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    project_name = models.CharField(max_length=128, default=project_id.name, auto_created=True, verbose_name='项目名')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "问题类型"
        verbose_name_plural = "问题类型"


class ProjectMission(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    mission_test = models.TextField(verbose_name='任务内容')
    mission_title = models.CharField(max_length=128, verbose_name='任务标题')
    pre_mission = models.ForeignKey('ProjectMission', on_delete=models.CASCADE, related_name='it_pre',
                                    verbose_name='前驱任务', default=None)
    member_id = models.ForeignKey('ProjectMember', on_delete=models.CASCADE, verbose_name='所属项目成员')
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    mission_process = models.PositiveIntegerField(verbose_name='任务进度', default=0, auto_created=True)
    belong_mission_id = models.ForeignKey('ProjectMission', on_delete=models.CASCADE, related_name='it_belong_to',
                                          verbose_name='所属任务', )
    start_time = models.DateField(verbose_name='开始时间')
    pre_end_time = models.TimeField(verbose_name='预计结束时间')
    mission_weight = models.PositiveIntegerField(verbose_name='任务权重', default=0, auto_created=True)
    end_time = models.DateTimeField(verbose_name='结束时间', default=None, auto_created=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目任务"
        verbose_name_plural = "项目任务"


class ProjectFile(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="文件名")
    description = models.TextField(verbose_name="文件描述")
    url = models.FileField(upload_to='uploads/', verbose_name="文件")
    upload_user_name = models.CharField(max_length=128, verbose_name="上传人名")
    project_name = models.CharField(max_length=128, verbose_name="所属项目名")
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="所属项目ID")
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="所属用户ID")
    mission_id = models.ForeignKey('ProjectMission', on_delete=models.CASCADE, verbose_name="所属任务ID")
    member_id = models.ForeignKey('ProjectMember', on_delete=models.CASCADE, verbose_name="所属项目成员ID")
    download_times = models.PositiveIntegerField(verbose_name="下载记录", default=0, auto_created=True)
    upload_time = models.DateTimeField(auto_now=True, verbose_name="上传时间")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目文件"
        verbose_name_plural = "项目文件"


class ProjectMember(models.Model):
    power_choice = (
        (0, '成员'),
        (1, '管理员'),
        (2, '项目主')
    )
    id = models.PositiveIntegerField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户ID')
    user_name = models.CharField(max_length=128, verbose_name='用户名')
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目ID')
    project_name = models.CharField(max_length=128, verbose_name='项目名')
    member_cost = models.PositiveIntegerField(verbose_name='成本', default=0, auto_created=True)
    member_power = models.CharField(max_length=128, verbose_name='权限', choices=power_choice, default=0)
    join_time = models.TimeField(auto_now_add=True, verbose_name='加入时间')
    exit_time = models.TimeField(verbose_name='退出时间', default=None, auto_created=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目成员"
        verbose_name_plural = "项目成员"


class ProjectResource(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=128, verbose_name='资源类型')
    description = models.CharField(max_length=128, verbose_name='资源描述')
    cost = models.PositiveIntegerField(verbose_name='资源成本')
    use_resource = models.PositiveIntegerField(verbose_name='已用资源')
    no_use_resource = models.PositiveIntegerField(verbose_name='未用资源')
    resource_unit = models.CharField(max_length=128, verbose_name='单位')
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    member_id = models.ForeignKey('ProjectMission', on_delete=models.CASCADE, verbose_name="所属项目成员ID")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目资源"
        verbose_name_plural = "项目资源"


class ProjectCalendar(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='所属项目')
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='所属用户')
    member_id = models.ForeignKey('ProjectMission', on_delete=models.CASCADE, verbose_name="所属项目成员ID")
    job_hour = models.PositiveIntegerField(verbose_name='工作时间', default=0, )
    week_number = models.CharField(max_length=128, verbose_name='星期数')
    is_job_day = models.BooleanField(verbose_name='是否为工作日')
    per_hour_money = models.PositiveIntegerField(verbose_name='每小时成本')
    date_time = models.DateTimeField(verbose_name='日期')
    job_log = models.TextField(verbose_name='工作日志')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    f_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "项目日历"
        verbose_name_plural = "项目日历"

# class Gantt(models.Model):
#     class Meta:
#         ordering = ["-c_time"]
#         verbose_name = "甘特图"
#         verbose_name_plural = "甘特图"
#
#
# class NetChart(models.Model):
#     class Meta:
#         ordering = ["-c_time"]
#         verbose_name = "网络图"
#         verbose_name_plural = "网络图"
