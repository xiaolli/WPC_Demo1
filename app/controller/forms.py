from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SelectField,RadioField,DateTimeField,DateField,SubmitField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.validators import DataRequired


class loginForm(FlaskForm):
    login_name = StringField('login_name',validators=[DataRequired()])
    login_password = PasswordField('login_password',validators=[DataRequired()])


class collectForm(FlaskForm):
    emp_SN=StringField('emp_SN', validators=[DataRequired()])
    emp_name=StringField('emp_name', validators=[DataRequired()])
    submit =SubmitField('Add')

'''
    emp_mail=StringField('emp_mail', validators=[DataRequired()])
    emp_role=StringField('emp_role', validators=[DataRequired()])
    emp_project=StringField('emp_project', validators=[DataRequired()])
    emp_team = StringField('emp_team', validators=[DataRequired()])
    emp_onboard_date = DateField('emp_onboard_date',validators=[DataRequired()])
    emp_IBM_joinDate = DateField('emp_IBM_joinDate',validators=[DataRequired()])
    emp_Phone = StringField('emp_Phone', validators=[DataRequired()])
    emp_Skill = SelectField('emp_Skill', validators=[DataRequired()],choices=[('', ''),
                                                                              ('MainFrame', 'MainFrame'),
                                                                              ('JAVA','JAVA')])
    emp_language = SelectField('emp_language', validators=[DataRequired()],choices=[('0',''),
                                                                                    ('1', 'English'),
                                                                                    ('2','Japanese')])
    emp_Band = SelectField('emp_band', validators=[DataRequired()],choices=[('0', ''),
                                                                            ('1', '6H'),('2','6A'),('3','6B'),
                                                                            ('4','7A'),('5','7B'),('6','8')])

    emp_photo_title = StringField('emp_photo_title',validators=[DataRequired()])
    emp_photo_image = FileField('emp_phono_image',validators=[FileRequired('No file is selected!')])
    emp_photo_creatdate = DateField('emp_photo_creatdate',validators=[DataRequired()])
    emp_photo_flag = BooleanField('emp_photo_groupflag',validators=[DataRequired()],default=False)

    emp_video_title = StringField('emp_video_title',validators=[DataRequired()])
    emp_video_image = FileField('emp_video_image',validators=[FileRequired('No file is selected!')])
    emp_video_creatdate = DateField('emp_video_creatdate',validators=[DataRequired()])

    emp_audio_title = StringField('emp_audio_title',validators=[DataRequired()])
    emp_audio_image = FileField('emp_audio_image',validators=[FileRequired('No file is selected!')])
    emp_audio_creatdate = DateField('emp_audio_creatdate',validators=[DataRequired()])

    submit =SubmitField('Add')
    reset = SubmitField('Reset')'''
