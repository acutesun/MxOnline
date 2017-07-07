from django import forms
from opreation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):  # 验证提交表单数据

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']  # 需要验证模型的字段

    def clean_mobile(self):  # 方法必须以clean开头加上要验证模型的字段
        mobile = self.cleaned_data['mobile']  # 存储模型字段的字典
        regex_moblie = '^1[34578]\d{9}$'   # 手机号正则
        if re.match(regex_moblie, mobile):
            return mobile
        else:
            raise forms.ValidationError('非法手机号', code='invalid_moblie')

