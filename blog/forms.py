from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class PostForm(FlaskForm):
    title = StringField('文章标题', validators=[
        DataRequired(message="标题不能为空"),
        Length(max=100, message="标题最长100字")
    ])
    content = TextAreaField('文章内容', validators=[
        DataRequired(message="内容不能为空"),
        Length(min=10, message="内容至少10字")
    ])
    submit = SubmitField('立即发布')
