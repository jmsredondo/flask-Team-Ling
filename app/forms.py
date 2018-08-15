from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Form
from wtforms.validators import *
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(Form):
    firstname = StringField('Firstname',
                            validators=[DataRequired()
                                        ])

    lastname = StringField('Lastname',
                           validators=[DataRequired()
                                       ])

    username = StringField('Username',
                           validators=[DataRequired(),
                                        Regexp('^(?=.*?([a-z)(?=.*?[_])]+)$')
                                       ])

    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Regexp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
                                    ])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         InputRequired(),
                                         Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$')
                                         ])

    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password', message="Password Must Match")
                                          ])
    phone = StringField('Phone',
                        validators=[Regexp('([0-9])'),
                                    Length(min=11, max=11)
                                    ])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BookForm(Form):
    bookName = StringField('Book Name',
                            validators=[DataRequired()])

    image = StringField('Image')

    description = StringField('Description')

    submit = SubmitField('Add Book')


