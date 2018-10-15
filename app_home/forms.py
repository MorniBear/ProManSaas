from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.Form):
    email = forms.CharField(max_length=128,
                            widget=forms.EmailInput(
                                attrs={'id': 'inputEmail', 'required': 'required', 'class': 'form-control',
                                       'style': 'width: 85%',
                                       'placeholder': '请输入电子邮箱'}))
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(
                                   attrs={'id': 'inputPassword', 'required': 'required', 'class': 'form-control',
                                          'style': 'width: 85%',
                                          'placeholder': '请输入密码'}))


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=128,
                           widget=forms.TextInput(
                               attrs={'id': 'inputName', 'required': 'required', 'class': 'form-control',
                                      'style': 'width: 85%',
                                      'placeholder': '请输入用户名'}))
    # head_icon = forms.ImageField()
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'inputEmail', 'required': 'required', 'class': 'form-control',
                                       'style': 'width: 85%',
                                       'placeholder': '请输入邮箱'}))
    # true_name = forms.CharField(max_length=128,
    #                             widget=forms.TextInput(
    #                                 attrs={'id': 'inputTrueName', 'required': 'required', 'class': 'form-control',
    #                                        'style': 'width: 85%',
    #                                        'placeholder': '请输入真实姓名'}))
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(
                                   attrs={'id': 'inputPassword', 'required': 'required', 'class': 'form-control',
                                          'style': 'width: 85%',
                                          'placeholder': '请输入密码'}))
    password_confirm = forms.CharField(max_length=128,
                                       widget=forms.PasswordInput(
                                           attrs={"aria-describedby": 'button-addon2',
                                                  'id': 'inputPasswordConfirm', 'required': 'required',
                                                  'class': 'form-control',
                                                  'style': 'width: 85%;margin-top: 1%',
                                                  'placeholder': '确认密码'}))
    code = forms.CharField(max_length=128,
                           widget=forms.TextInput(
                               attrs={'id': 'inputCode', 'required': 'required', 'class': 'form-control',
                                      'placeholder': '验证码'}))
