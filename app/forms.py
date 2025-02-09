# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Email, EqualTo, Length

# class SignupForm(FlaskForm):
#     username = StringField("Username", validators=[InputRequired(), Length(min=3, max=50)])
#     email = StringField("Email", validators=[InputRequired(), Email()])
#     password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
#     confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
#     submit = SubmitField("Sign Up")

# class LoginForm(FlaskForm):
#     email = StringField("Email", validators=[InputRequired(), Email()])
#     password = PasswordField("Password", validators=[InputRequired()])
#     submit = SubmitField("Log In")

#