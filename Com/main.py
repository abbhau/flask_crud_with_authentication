from flask import Flask, redirect, url_for, render_template, request, flash, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
app  = Flask(__name__)


with app.app_context():
    
    app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:root@127.0.0.1:3306/b41'
    app.config['SQLALCHEMY_TRACK_MODIFICAIONS'] = False
    app.config['SECRET_KEY'] = 'jdabdibcjhcbjs'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'loginview'

    db = SQLAlchemy(app)
    class Student(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        roll = db.Column(db.Integer)
        name = db.Column(db.String(60))
        marks = db.Column(db.Float)

    class User(db.Model, UserMixin):
        user_id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(60), nullable = False)
        password= db.Column(db.String(60), nullable = False)
    
    class User1(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(60), nullable = False)
        password= db.Column(db.String(60), nullable = False)
    
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return User1.query.filter_by(id=user_id).first()

@app.route('/add', methods=['GET', 'POST'])
@login_required
def student_add_view():
    if request.method=='POST':
        rn = request.form.get('roll')
        nm = request.form.get('name')
        mk = request.form.get('marks')
        stu = Student(roll=rn, name=nm, marks=mk)
        db.session.add(stu)
        db.session.commit()
        return redirect(url_for('show_student'))
    return render_template('student_form.html')

@app.route('/show_student', methods=['GET'])
@login_required
def show_student():
    obj = Student.query.all()
    return render_template('show_student.html', rec=obj)

@app.route('/up_stu/<int:id>', methods=['GET', 'POST'])
@login_required
def up_stu_view(id):
    obj = Student.query.get(id)
    if request.method=='POST':
        obj.roll = request.form.get('roll')
        obj.name = request.form.get('name')
        obj.marks =  request.form.get('marks')
        db.session.commit()
        return redirect(url_for('show_student'))
    return render_template('upd_stu_form.html', rec=obj)

@app.route('/del_student/<int:id>', methods=['GET', 'POST'])
@login_required
def del_stu_view(id=None):
    if request.method=='POST':
        obj = Student.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for('show_student'))
    return render_template('delete_student_confirm.html')

@app.route('/signup', methods=['GET', 'POST'])
def registerview():
    if request.method=='POST':
        us = request.form.get('username')
        ps = request.form.get('password')
        user = User1(username=us, password=ps)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('loginview'))
    return render_template('register_form.html')

@app.route('/login', methods=['GET', 'POST'])
def loginview():
    if request.method=='POST':
        us = request.form.get('username')
        ps = request.form.get('password')
        user = User1.query.filter_by(username=us, password=ps).first()
        if user:
            login_user(user)
            return redirect(url_for('show_student'))
        else:
            flash('invalid credentials', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/show', methods=['GET'])
def show_stu():
    obj = Student.query.all()
    data = [{"id":i.id, "roll":i.roll , "name":i.name, "marks":i.marks } for i in obj]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
