# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditPersonForm, CreatePersonForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Employee
from werkzeug.urls import url_parse
import sqlalchemy as sa
from sqlalchemy import and_


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home Page")


@app.route('/table')
@login_required
def table():
    employees = db.session.query(Employee).all()
    return render_template('table.html', title="Table view", employees=employees)


@app.route('/api/data')
@login_required
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
        if col_name not in ['name', 'work_positon', 'date_join', 'wage', 'chief_name']:
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


@app.route('/person/<id>', methods=['GET', 'POST'])
@login_required
def get_employee(id: str):
    if not id or not id.isdigit():
        return redirect(url_for('create_person'))
    employee = db.session.query(Employee).filter(Employee.id == id).all()
    if not len(employee):
        return redirect(url_for('create_person'))
    person: Employee = employee[0]
    form = EditPersonForm(obj=person)
    if person.chief_name:
        form.chief_name.choices = [f"{person.chief_name}_{person.chief.date_join}"]
    if form.validate_on_submit():
        childs = db.session.query(Employee).filter(Employee.chief_id == person.id).all()
        if form.edit.data:
            if form.chief_name.data:
                chief_name_form, chief_date_form = form.chief_name.data.split('_')
                chief = db.session.query(Employee).filter(
                    and_(Employee.name == chief_name_form, Employee.date_join == chief_date_form)).all()[0]
                chief_id = chief.id
                chief_name = chief.name
            else:
                chief_id = None
                chief_name = ''
            person.name = form.name.data
            person.work_position = form.work_position.data
            person.date_join = form.date_join.data
            person.wage = form.wage.data
            person.chief_id = chief_id
            person.chief_name = chief_name
            db.session.commit()
            flash("User changet")
            return redirect(url_for('get_employee', id=id))

        if form.delete.data:
            for child in childs:
                child.chief_name = person.chief_name
                child.chief_id = person.chief_id
                child.chief = person.chief
                db.session.add(child)
            db.session.query(Employee).filter(Employee.id == person.id).delete()
            db.session.commit()
            return redirect(url_for('table'))
    return render_template('person.html', title="Person info", person=person, form=form)


@app.route('/create_person', methods=["GET", "POST"])
@login_required
def create_person():
    form = CreatePersonForm()
    if form.validate_on_submit():
        if form.chief_name.data:
            chief_name_form, chief_date_form = form.chief_name.data.split('_')
            chief = db.session.query(Employee).filter(
                and_(Employee.name == chief_name_form, Employee.date_join == chief_date_form)).all()[0]
            chief_id = chief.id
            chief_name = chief.name
        else:
            chief_id = None
            chief_name = ''
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # photo upload func is not realized
        person = Employee(name=form.name.data, work_position=form.work_position.data, date_join=form.date_join.data,
                          wage=form.wage.data, chief_id=chief_id, chief_name=chief_name)
        db.session.add(person)
        db.session.commit()
        flash("User added")
        return redirect(url_for('create_person'))

    return render_template('person.html', title="Create employee form ", form=form)


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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/api/get_employeers')
def get_employeers():
    """:return list of childs of employeers if exist id_chief or list of top boss"""
    query = Employee.query
    # search filter
    search = request.args.get('id_chief')
    if search.isnumeric():
        query = query.filter(Employee.chief_id == search)
    else:
        query = query.filter(Employee.chief_id == sa.null())
    return {
        'data': [employee.to_dict() for employee in query],
        # 'draw': request.args.get('draw', type=int),
    }


@app.route('/api/get_list_by_filter_names')
def get_list_by_filter_names():
    """:return list of childs of employeers if exist id_chief or list of top boss"""
    # search filter
    search = request.args.get('name')
    query = Employee.query.filter(Employee.name.like(f"%{search}%"))
    return {
        'data': [employee.to_dict() for employee in query],
    }
