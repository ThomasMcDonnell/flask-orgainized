from flask import (render_template, flash, url_for, redirect, request,
                   Response, abort)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TodoForm
from app.models import User, Todo
from datetime import datetime
import json


# Home view 
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    form = TodoForm()
    if form.validate_on_submit():
        #create todo and add to the database 
        todo = Todo(name=form.name.data, start=form.start.data,
                    end=form.end.data, actionable=form.actionable.data,
                    author=current_user)
        db.session.add(todo)
        db.session.commit()
        flash('Event has been created')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', todos=todos, form=form)


# Last seen update 
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_active = datetime.utcnow()
        db.session.commit()


# User calendar view
@app.route('/calendar/<username>')
@login_required
def calendar(username):
    user = User.query.filter_by(username=username).first_or_404()
    todos = Todo.query.filter_by(user_id=user.id).all()
    return render_template('calendar.html', user=user, todos=todos, title='Calendar')


# Delete an event
@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.author != current_user:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash('Event has been deleted')
    return redirect(url_for('index'))


# api type endpoint for fullcalender.js
@app.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    callist = list()
    for row in todos:
        callist.append({'title': row.name, 'start': str(row.start), 'end':
                        str(row.end), 'description': row.actionable})
    return Response(json.dumps(callist),  mimetype='application/json')


# Register a user account 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #add the user to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if user logged in and tries to access login page redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #query the database for user
        user = User.query.filter_by(username=form.username.data).first()
        #if user not in database or password incorrect redirect to login
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #login user
        next_page = request.args.get('next')
        #parse query string to determine path relative or absolute
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# User logout 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
