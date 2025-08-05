# -*- coding: utf-8 -*-
"""
AgriDec 表单定义
用户认证和数据输入表单
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from .models import User

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=80, message='用户名长度应在3-80个字符之间')
    ], render_kw={'placeholder': '请输入用户名', 'class': 'form-control'})
    
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, message='密码长度至少6个字符')
    ], render_kw={'placeholder': '请输入密码', 'class': 'form-control'})
    
    remember_me = BooleanField('记住我', render_kw={'class': 'form-check-input'})
    
    submit = SubmitField('登录', render_kw={'class': 'btn btn-primary w-100'})

class RegisterForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=80, message='用户名长度应在3-80个字符之间')
    ], render_kw={'placeholder': '请输入用户名', 'class': 'form-control'})
    
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ], render_kw={'placeholder': '请输入邮箱', 'class': 'form-control'})
    
    real_name = StringField('真实姓名', validators=[
        DataRequired(message='请输入真实姓名'),
        Length(min=2, max=100, message='姓名长度应在2-100个字符之间')
    ], render_kw={'placeholder': '请输入真实姓名', 'class': 'form-control'})
    
    phone = StringField('手机号码', validators=[
        Optional(),
        Length(min=11, max=11, message='请输入11位手机号码')
    ], render_kw={'placeholder': '请输入手机号码', 'class': 'form-control'})
    
    region = SelectField('所在地区', validators=[
        DataRequired(message='请选择所在地区')
    ], choices=[
        ('北京市', '北京市'),
        ('天津市', '天津市'),
        ('河北省', '河北省'),
        ('山西省', '山西省'),
        ('内蒙古', '内蒙古'),
        ('辽宁省', '辽宁省'),
        ('吉林省', '吉林省'),
        ('黑龙江省', '黑龙江省'),
        ('上海市', '上海市'),
        ('江苏省', '江苏省'),
        ('浙江省', '浙江省'),
        ('安徽省', '安徽省'),
        ('福建省', '福建省'),
        ('江西省', '江西省'),
        ('山东省', '山东省'),
        ('河南省', '河南省'),
        ('湖北省', '湖北省'),
        ('湖南省', '湖南省'),
        ('广东省', '广东省'),
        ('广西', '广西'),
        ('海南省', '海南省'),
        ('重庆市', '重庆市'),
        ('四川省', '四川省'),
        ('贵州省', '贵州省'),
        ('云南省', '云南省'),
        ('西藏', '西藏'),
        ('陕西省', '陕西省'),
        ('甘肃省', '甘肃省'),
        ('青海省', '青海省'),
        ('宁夏', '宁夏'),
        ('新疆', '新疆')
    ], render_kw={'class': 'form-select'})
    
    farm_type = SelectField('农场类型', validators=[
        DataRequired(message='请选择农场类型')
    ], choices=[
        ('种植业', '种植业'),
        ('养殖业', '养殖业'),
        ('混合农业', '混合农业'),
        ('果园', '果园'),
        ('蔬菜种植', '蔬菜种植'),
        ('粮食作物', '粮食作物'),
        ('经济作物', '经济作物'),
        ('其他', '其他')
    ], render_kw={'class': 'form-select'})
    
    farm_size = FloatField('农场规模（亩）', validators=[
        Optional(),
        NumberRange(min=0.1, max=10000, message='农场规模应在0.1-10000亩之间')
    ], render_kw={'placeholder': '请输入农场规模', 'class': 'form-control', 'step': '0.1'})
    
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, max=128, message='密码长度应在6-128个字符之间')
    ], render_kw={'placeholder': '请输入密码', 'class': 'form-control'})
    
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ], render_kw={'placeholder': '请再次输入密码', 'class': 'form-control'})
    
    submit = SubmitField('注册', render_kw={'class': 'btn btn-success w-100'})
    
    def validate_username(self, username):
        """验证用户名唯一性"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名')
    
    def validate_email(self, email):
        """验证邮箱唯一性"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')

class ProfileForm(FlaskForm):
    """用户资料编辑表单"""
    real_name = StringField('真实姓名', validators=[
        DataRequired(message='请输入真实姓名'),
        Length(min=2, max=100, message='姓名长度应在2-100个字符之间')
    ], render_kw={'class': 'form-control'})
    
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ], render_kw={'class': 'form-control'})
    
    phone = StringField('手机号码', validators=[
        Optional(),
        Length(min=11, max=11, message='请输入11位手机号码')
    ], render_kw={'class': 'form-control'})
    
    region = SelectField('所在地区', validators=[
        DataRequired(message='请选择所在地区')
    ], choices=[
        ('北京市', '北京市'),
        ('天津市', '天津市'),
        ('河北省', '河北省'),
        ('山西省', '山西省'),
        ('内蒙古', '内蒙古'),
        ('辽宁省', '辽宁省'),
        ('吉林省', '吉林省'),
        ('黑龙江省', '黑龙江省'),
        ('上海市', '上海市'),
        ('江苏省', '江苏省'),
        ('浙江省', '浙江省'),
        ('安徽省', '安徽省'),
        ('福建省', '福建省'),
        ('江西省', '江西省'),
        ('山东省', '山东省'),
        ('河南省', '河南省'),
        ('湖北省', '湖北省'),
        ('湖南省', '湖南省'),
        ('广东省', '广东省'),
        ('广西', '广西'),
        ('海南省', '海南省'),
        ('重庆市', '重庆市'),
        ('四川省', '四川省'),
        ('贵州省', '贵州省'),
        ('云南省', '云南省'),
        ('西藏', '西藏'),
        ('陕西省', '陕西省'),
        ('甘肃省', '甘肃省'),
        ('青海省', '青海省'),
        ('宁夏', '宁夏'),
        ('新疆', '新疆')
    ], render_kw={'class': 'form-select'})
    
    farm_type = SelectField('农场类型', validators=[
        DataRequired(message='请选择农场类型')
    ], choices=[
        ('种植业', '种植业'),
        ('养殖业', '养殖业'),
        ('混合农业', '混合农业'),
        ('果园', '果园'),
        ('蔬菜种植', '蔬菜种植'),
        ('粮食作物', '粮食作物'),
        ('经济作物', '经济作物'),
        ('其他', '其他')
    ], render_kw={'class': 'form-select'})
    
    farm_size = FloatField('农场规模（亩）', validators=[
        Optional(),
        NumberRange(min=0.1, max=10000, message='农场规模应在0.1-10000亩之间')
    ], render_kw={'class': 'form-control', 'step': '0.1'})
    
    submit = SubmitField('保存', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        """验证邮箱唯一性（排除当前用户）"""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该邮箱已被其他用户使用')

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    current_password = PasswordField('当前密码', validators=[
        DataRequired(message='请输入当前密码')
    ], render_kw={'class': 'form-control'})
    
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, max=128, message='密码长度应在6-128个字符之间')
    ], render_kw={'class': 'form-control'})
    
    new_password2 = PasswordField('确认新密码', validators=[
        DataRequired(message='请确认新密码'),
        EqualTo('new_password', message='两次输入的新密码不一致')
    ], render_kw={'class': 'form-control'})
    
    submit = SubmitField('修改密码', render_kw={'class': 'btn btn-warning'})

class DataCollectionForm(FlaskForm):
    """数据采集表单"""
    website = SelectField('数据源', validators=[
        DataRequired(message='请选择数据源')
    ], choices=[
        ('seed_trade', '中国种子交易网'),
        ('weather', '中国天气网'),
        ('farm_machine', '农机360网')
    ], render_kw={'class': 'form-select'})
    
    region = SelectField('地区', validators=[
        DataRequired(message='请选择地区')
    ], choices=[
        ('全国', '全国'),
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('南京', '南京'),
        ('山东', '山东'),
        ('河南', '河南'),
        ('河北', '河北'),
        ('江苏', '江苏'),
        ('安徽', '安徽')
    ], render_kw={'class': 'form-select'})
    
    max_pages = SelectField('采集页数', validators=[
        DataRequired(message='请选择采集页数')
    ], choices=[
        ('1', '1页'),
        ('2', '2页'),
        ('3', '3页'),
        ('5', '5页')
    ], render_kw={'class': 'form-select'})
    
    submit = SubmitField('开始采集', render_kw={'class': 'btn btn-success'})
