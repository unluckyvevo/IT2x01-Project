from flask import render_template, url_for, flash, redirect, request
from readbit import app, db, bcrypt
from readbit.forms import LoginForm
from readbit.models import User
from flask_login import login_user, current_user, logout_user, login_required
import typing

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:
        if current_user.type == 'student':
            return redirect(url_for('dashboard'))
        return redirect(url_for('module_list'))
        
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(url_for(next_page[1:]))

            else:
                return redirect(url_for('dashboard')) if current_user.type == 'student' else redirect(
                    url_for('module_list'))

        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Personal Dashboard')

@app.route('/module_list')
def module_list():
    """
    Added by Dylan Woo
    Student cannot manage modules
    """
    if current_user.type == 'student':
        return redirect(url_for('dashboard'))
        
    modulelist: typing.List[int] = [1,2,3,4,5,6,7]
    return render_template('module_list.html', title='Module List', modulelist=modulelist)

@app.route('/class_dashboard')
def class_dashboard():
    classlist: typing.List[int] = [1,2,3,4,5,6]
    return render_template('class_dashboard.html', title='Class Dashboard', classlist=classlist)

@app.route('/view_component_scores')
def view_component_scores():
    module_name = "Module"
    component_name = "Component"
    return render_template('view_component_scores.html', title='View Component Scores', module_name=module_name, component_name=component_name)

@app.route('/manage_feedback')
def manage_feedback():
    module_name: typing.List[str] = "Module"
    component_name: typing.List[str] ="Component"
    teaching_classlist: typing.List[str] = ['T1','T2','T3','T4','T5', 'T6']
    return render_template('manage_feedback.html', title='Manage Feedback', module_name=module_name, component_name=component_name, teaching_classlist=teaching_classlist)


@app.route('/manage_class')
def manage_class():
    """
    Added by Dylan Woo
    Student cannot manage modules
    """
    if current_user.type == 'student':
        return redirect(url_for('dashboard'))

    teaching_classlist: typing.List[str] = ['T1','T2','T3','T4','T5', 'T6']
    return render_template('manage_class.html', title='Manage Class', teaching_classlist=teaching_classlist)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

"""
Added by Dylan Woo
"""
@app.route('/manage_module')
def manage_module():
    """
        Student cannot manage modules
    """
    if current_user.type == 'student':
            return redirect(url_for('dashboard'))

    assessments: typing.List[typing.Dict] = [{
        "Quiz 1": {
            "Weightage": "5%",
            "Date": "20/10/2020"
        },

        "Quiz 2": {
            "Weightage": "5%",
            "Date": "20/10/2020"
        }
    }]
    return render_template('manage_module.html', title='Manage Module', assessments=assessments)

@app.route('/add_student_manually')
def add_student_manually():
    return render_template('add_student_manually.html', title='Add Student Manually')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html', title='Student Dashboard')

@app.route('/add_marks')
def add_marks():
    teaching_classlist: typing.List[str] = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    module = 'Module'
    component = 'Quiz 1'
    return render_template('add_marks.html', title='Add Marks',teaching_classlist=teaching_classlist, module=module, component=component)