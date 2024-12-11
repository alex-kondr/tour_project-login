from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    username = wtforms.StringField("Введіть логін або email", validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField("Увійти")


class SingUpForm(FlaskForm):
    username = wtforms.StringField("Введіть свій логін")
    email = wtforms.EmailField("Введіть свою електронну адресу", validators=[wtforms.validators.DataRequired("Обов'язково"), wtforms.validators.Email()])
    password = wtforms.PasswordField("Пароль", validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField("Зареєструватись")


# login_form = Login()
# singup_form = SingUp()