from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from plant_collection.forms import UserLoginForm, UserSignupForm
from plant_collection.models import db, User
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, email, password)

            # creating/adding user to database
            user = User( email,first_name,last_name,  password = password) #changing to this order helped to enter into correct db columns(maybe b/c of init in models)
            db.session.add(user)
            db.session.commit()
            
            flash(f'You have successfully created a user account for {email}. \nWelcome to The Plant Collection!', "user-created")
            return redirect(url_for('site.home'))   #maybe change redirect to profile(maybe even pop up option to choose)
                                            # will probably leave as redirect to home to allow user to explore
    except:
        raise Exception('Invalid Form Data: Please check your info...')

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email==email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please check your form...')

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

