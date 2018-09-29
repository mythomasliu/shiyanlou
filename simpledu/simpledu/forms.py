from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms import TextAreaField,IntegerField
from wtforms.validators import Length,Email,EqualTo,Required, ValidationError
from wtforms.validators import URL,NumberRange
from simpledu.models import db,User,Course

class RegisterForm(FlaskForm):
    username = StringField('username',validators=[Required(),Length(3,24)])
    email = StringField('email',validators=[Required(),Email()])
    password = PasswordField('password',validators=[Required(),Length(6,24)])
    repeat_password = PasswordField('repead_password',validators=[Required(),EqualTo('password')])
    submit = SubmitField('submit')
    
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username has exist!')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email has exist!')

    def create_user(self):
        user=User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('email',validators=[Required(),Email()])
    password = PasswordField('password',validators=[Required(),Length(6,24)])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')

    def validate_email(self,field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('The email not exist!')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('The password error')

class CourseForm(FlaskForm):
    name = StringField('course name',validators=[Required(),Length(5,32)])
    description = TextAreaField('course description',validators=[Required(),Length(10,256)])
    image_url = StringField('image',validators=[Required(),URL()])
    author_id = IntegerField('author id',validators=[Required(),NumberRange(min=1,message='invalid user id')])
    submit = SubmitField('submit')

    def validate_author_id(self,field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('The username not exist')
    
    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self,course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course
