# Generated by Django 2.1.1 on 2018-10-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_home', '0002_auto_20181002_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcheck',
            name='code',
            field=models.CharField(max_length=6, verbose_name='验证码'),
        ),
    ]
