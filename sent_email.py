import os

from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'ProManSaas.settings'


def send_proman_email(email, code):
    send_mail(
        '来自ProManSaas的验证',
        '您的验证码为：' + code,
        'mornibear@sina.com',
        [email],
    )
