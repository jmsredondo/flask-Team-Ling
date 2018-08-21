from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, InputRequired, EqualTo, ValidationError, Length
from models import User
from flask_wtf import FlaskForm


# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# # Login
# login = LoginManager(app)
# login.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired()]
                            )

    lastname = StringField('Lastname',
                           validators=[DataRequired()]
                           )

    username = StringField('Username',
                           validators=[DataRequired(),
                                       Regexp('(([a-z]|_)+)')
                                       ]
                           )

    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Regexp('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
                                    ]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         InputRequired(),
                                         Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$')
                                         ]
                             )

    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                                          EqualTo('password', message="Password Must Match")
                                          ]
                              )
    phone = StringField('Phone',
                        validators=[Regexp('([0-9])'),
                                    Length(min=11, max=11)
                                    ]
                        )

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BookForm(FlaskForm):
    bookName = StringField('Book Name',
                           validators=[DataRequired()])

    image = StringField('Image')

    description = StringField('Description')

    submit = SubmitField('Add Book')
