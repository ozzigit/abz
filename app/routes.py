# -*- coding: utf-8 -*-
import json
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Employee
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title="Home Page")


@app.route('/table')
@login_required
def table():
    employees = db.session.query(Employee).filter(Employee.name != 'Boss')
    return render_template('table.html', title="table view", employees=employees)


@app.route('/api/data')
def data():
    query = Employee.query
    # search filter
    search = request.args.get('search[value]')

    if search:
        query = query.filter(
            db.or_(
                db.or_(Employee.name.like(f'%{search}%'),
                       db.or_(Employee.date_join.like(f'%{search}%'),
                              db.or_(Employee.chief_name.like(f'%{search}%'),
                                     db.or_(Employee.work_position.like(f'%{search}%')),
                                     Employee.wage == search if search.isnumeric() else None)
                              )
                       )
            )
        )
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name', 'work_positon', 'date_join', 'wage', 'chief']:
            col_name = 'name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Employee, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [employee.to_dict() for employee in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Employee.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.route('/person/<id>')
@login_required
def get_employee(id):
    employee = db.session.query(Employee).filter(Employee.id == id).all()
    if len(employee):
        return f'name {employee[0].name}, id {employee[0].id}'
    return 'Not found'


@app.route('/get_childs/<id>')
@login_required
def get_childs(id):
    childs = db.session.query(Employee).filter(Employee.chief_id == id).all()
    chief = db.session.query(Employee).filter(Employee.id == id).all()
    if len(childs) and len(chief):
        return render_template('child.html', time="childs list", childs=childs, chief=chief[0])
    return "Not found"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
