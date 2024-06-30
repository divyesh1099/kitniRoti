from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def populate_from_json(self, json_data):
        self.username.data = json_data.get('username', '')
        self.email.data = json_data.get('email', '')
        self.password.data = json_data.get('password', '')
        self.confirm_password.data = json_data.get('confirm_password', '')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def populate_from_json(self, json_data):
        self.email.data = json_data.get('email', '')
        self.password.data = json_data.get('password', '')

class MealForm(FlaskForm):
    meal_type = SelectField('Meal Type', choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], validators=[DataRequired()])
    rotis = IntegerField('Number of Rotis', validators=[DataRequired()])
    sabjis = StringField('Sabjis')
    rice = StringField('Rice')
    special_dish = StringField('Special Dish')
    milk = StringField('Milk')
    submit = SubmitField('Add Meal')

    def populate_from_json(self, json_data):
        self.meal_type.data = json_data.get('meal_type', '')
        self.rotis.data = json_data.get('rotis', 0)
        self.sabjis.data = json_data.get('sabjis', '')
        self.rice.data = json_data.get('rice', '')
        self.special_dish.data = json_data.get('special_dish', '')
        self.milk.data = json_data.get('milk', '')
