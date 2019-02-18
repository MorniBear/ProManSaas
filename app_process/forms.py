from django import forms


class MissionFrom(forms.Form):
    member_choice = (
        ('0', 'MorniBear'),
        ('1', 'MorniBear2')
    )
    mission_description = forms.CharField(
        widget=forms.Textarea(
            attrs={'style': "resize:none", 'class': "form-control", 'id': "validationCustom02", 'rows': 5,
                   'required': 'required'}
        )
    )
    mission_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'id': "mission_name",
                'type': "text",
                'class': "form-control",
                'placeholder': "输入任务名",
                'aria - label': "输入任务名",
                'aria - describedby': "button-addon2",
            }
        )

    )
    member = forms.ChoiceField(
        choices=member_choice,
        widget=forms.Select(attrs={'id': 'power', 'required': 'required',
                                   'class': "form-control"}))
    start_time = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'id': 'start_time', 'required': 'required', 'class': "form-control"}))
    pre_end_time = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'id': 'pre_end_time', 'required': 'required', 'class': "form-control"}))


class MemberFrom(forms.Form):
    power_choice = (
        ('0', '成员'),
        ('1', '管理员')
    )
    user_power = forms.ChoiceField(
        choices=power_choice,
        widget=forms.Select(attrs={'id': 'power', 'required': 'required',
                                   'class': "form-control"}))
    user_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'id': "username",
                'type': "text",
                'class': "form-control",
                'placeholder': "输入用户名",
                'aria - label': "输入用户名",
                'aria - describedby': "button-addon2",
            }
        )

    )


class StartFrom(forms.Form):
    project_state = (
        ('0', "设想状态"),
        ('2', "准备状态"),
        ('3', "开始状态"),
        ('4', "停滞状态"),
    )
    project_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'validationCustom01', 'required': 'required', 'class': "form-control"}
        )
    )
    start_time = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'id': 'start_time', 'required': 'required', 'class': "form-control"}))
    pre_end_time = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'id': 'pre_end_time', 'required': 'required', 'class': "form-control"}))
    project_state = forms.ChoiceField(
        choices=project_state,
        widget=forms.Select(attrs={'id': 'inputState', 'required': 'required',
                                   'class': "form-control"}))

    project_description = forms.CharField(
        widget=forms.Textarea(
            attrs={'style': "resize:none", 'class': "form-control", 'id': "validationCustom02", 'rows': 5,
                   'required': 'required'}
        )
    )
