from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from flask_login import LoginManager, login_user, logout_user
from flask_migrate import Migrate
from flask_script import Manager

app = Flask(__name__, template_folder='templates2')

class MyForm(FlaskForm):
    username = StringField('USERNAME', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    city = StringField('CITY', validators=[DataRequired()])

    def validate_city(self, city):
        if len(str(city)) < 2:
            raise ValidationError('Len must be greater than 2')
        #elif not str(city).isalpha():
            #raise ValidationError('contain only characters')
        
        
with app.app_context():
   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/b43'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SECRET_KEY'] = 'gyjguguuhu'
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'loginview'

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db')

    class User(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(100), nullable=False)
        password = db.Column(db.String(255), nullable=False)
        city =  db.Column(db.String(100), nullable=False)

        def set_password(self, password):
            self.password = generate_password_hash(password)
        
        def check_password(self, password):
            return check_password_hash(self.password, password)

    class User1(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(100), nullable=False)
        password = db.Column(db.String(255), nullable=False)
        city =  db.Column(db.String(100), nullable=False)

        def set_password(self, password):
            self.password = generate_password_hash(password)
        
        def check_password(self, password):
            return check_password_hash(self.password, password)   
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return User1.query.filter_by(id=user_id).first()

@app.route('/add/user', methods=['POST', 'GET'])
def addUser():
    form = MyForm()
    if form.validate_on_submit():
        us = form.username.data
        ps = form.password.data
        ct = form.city.data
        user = User1(username=us,city=ct)
        user.set_password(ps)
        db.session.add(user)
        db.session.commit()
        return "success"
    return render_template('reg.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginview():
    if request.method=='POST':
        us = request.form.get('username')
        ps = request.form.get('password')
        user = User1.query.filter_by(username=us).first()
        if user and user.check_password(ps):
            login_user(user)
            return 'successfully login'
        else:
            flash('invalid credentials', 'danger')
            return render_template('login.html')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
    manager.run()
