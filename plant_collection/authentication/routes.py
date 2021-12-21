from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from plant_collection.forms import UserLoginForm, UserSignupForm, PlantForm
from plant_collection.models import db, User, Plant
from flask_login import login_user, logout_user, current_user, login_required
from ..api.routes import delete_plant

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
            
            flash(f'Success! You have created a user account for {email}. \nWelcome to The Plant Collection!', "success")
            return redirect(url_for('auth.signin'))
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
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('site.profile'))
            else:
                flash('ERROR! Your Email/Password is incorrect.', 'danger')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please check your form...')

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have successfully logged out!', "success")
            
    return redirect(url_for('site.home'))

@auth.route('/create', methods = ['GET', 'POST'])
@login_required
def new_plant():
    form = PlantForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            room = form.room.data
            plant_type = form.plant_type.data
            light = form.light.data
            description = form.description.data
            water = form.water.data
            fertilizer = form.fertilizer.data
            humidity = form.humidity.data
            pests = form.pests.data
            fun_fact = form.fun_fact.data
            user_token = current_user.token

            print(name, room, plant_type, light, description, water, fertilizer, humidity, pests, fun_fact)

            # creating/adding character to database
            plant = Plant(name, room, plant_type, light, description, water, fertilizer, humidity, pests, fun_fact, user_token)
            db.session.add(plant)
            db.session.commit()
            
            flash(f'Success! You have added "{name}" to your collection!', "success")
            return redirect(url_for('auth.new_plant')) # maybe change redirect to show plants
    except:
        raise Exception('Invalid Form Data: Please check your info...')

    return render_template('create.html', form = form)


@auth.route('/myplants')
@login_required
def show_plants(): 
    return render_template('show_all.html')

@auth.route('/plant/<plant_id>/update', methods = ['GET','POST'])
@login_required
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    form = PlantForm()
    if request.method == 'POST':
        plant.name = request.form['name']
        plant.room = request.form['room']
        plant.plant_type = request.form['plant_type']
        plant.light = request.form['light']
        plant.description = request.form['description']
        plant.water = request.form['water']
        plant.fertilizer = request.form['fertilizer']
        plant.humidity = request.form['humidity']
        plant.pests = request.form['pests']
        plant.fun_fact = request.form['fun_fact']

        db.session.commit()
        flash(f" Success! Your plant '{plant.name}' has been updated.", "success")
        return redirect(url_for('auth.show_plants'))
    return render_template('update_plant.html', plant=plant, form=form)


@auth.route('/plant/<plant_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    # add flash
    flash(f"Success! You have deleted '{plant.name}'.", "warning")
    return redirect(url_for('auth.show_plants'))
    

    # TEST DELETE ROUTE******************************* this kinda worked
# @auth.route('/delete', methods = ['GET', 'POST'])
# @login_required
# def delete_plant():
#     form = DeleteForm()
#     try:
#         if request.method == 'POST':
#             name = form.name.data
#             user_token = current_user.token

#             print(name)

#             # creating/adding character to database
#             plant = Plant(name, user_token)
#             db.session.delete(plant)
#             db.session.commit()
            
#             flash(f'You have successfully deleted {name}!', "plant-deleted")
#             return redirect(url_for('auth.get_my_plants'))
#     except:
#         raise Exception('Invalid Form Data: Please check your info...')

#     return render_template('delete_plant.html', form = form)


    # ANOTHER TEST************************
# @auth.route('/delete', methods = ['GET', 'POST'])
# @login_required
# def delete_plant():
#     form = DeleteForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         plant = Plant.query.filter_by(name=name).first_or_404()
#         try:
#             if request.method == 'POST':
#                 print('HELLO')
#                 delete_plant(current_user.token, plant.id )
#                 print('name, plant, plant.id')
#                 flash('Your changes have been saved.')
#                 return redirect(url_for('servers.delete', id=id))

#         except:
#             raise Exception('Invalid Form Data: Please check your info...')

#     return render_template('delete_plant.html', form=form)

# *****************LAST USED**************
# @auth.route('/delete', methods = ['GET', 'POST'])
# @login_required
# def delete_plant(name):
#     form = DeleteForm()
#     plant = Plant.query.get(name)
#     try:
#         if request.method == 'POST':
#             name = form.name.data
#             #plant = Plant.query.filter_by(name=name).first_or_404()
    
#             # if form.delete.data:
#             #     return redirect(url_for('servers.delete', id=id))

#             if form.validate_on_submit():
#                 delete_plant()
#                 flash('Your changes have been saved.')
#     except:
#          raise Exception('Invalid Form Data: Please check your info...')

#     return render_template('delete_plant.html', form=form)



# Endpoint Route and Function to delete a plant
# @auth.route('/delete', methods = ['GET', 'POST']) #might have to check these methods
# @login_required
# def delete_plant():
#     # make a form for deleting that asked for the name(check to make it unique)
#     # use form here get the name
#     form = DeleteForm
#     try:
#         if request.method == 'POST':
#             plant = form.name.data
#             print(plant)

#             db.session.delete(plant)
#             db.session.commit()

#             flash(f'You have successfully deleted {plant}!', "plant-deleted")
#             return redirect(url_for('auth.create'))
#     except:
#         raise Exception('Invalid Form Data: Please check your info...')
        
#     return render_template('delete_plant.html', form = form)
    
# Endpoint Route and Function to retrieve all plants
# try adding methods to update and delete at this endpoint
        # using the try/ if statement kinda like create function
   