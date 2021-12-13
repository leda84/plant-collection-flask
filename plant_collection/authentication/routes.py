from flask import Blueprint, render_template, request, redirect, url_for, flash
from plant_collection.forms import UserLoginForm, UserSignupForm
from plant_collection.models import db, User

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
            
            flash(f'You have successfully created a user account for {email}. \nWelcome to The Hero Project!', "user-created")
            return redirect(url_for('site.home'))   #maybe change redirect to profile(maybe even pop up option to choose)
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

            flash(f"You have successfully created a user account for {email}.", "user-created")
            return redirect(url_for('site.profile'))
    except:
        raise Exception('Invalid Form Data: Please check your form...')

    return render_template('signin.html', form = form)

