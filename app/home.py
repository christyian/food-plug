from flask import Blueprint, render_template, url_for, request, redirect, flash
from .models import Restaurant
from app.extentions import db  # import the database instance
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError


#create the home blue print
home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    return render_template('welcome.html')

@home.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@home.route('/listings')
@login_required
def listings():
    restaurants = Restaurant.query.all()
    return render_template('listingz.html', items=restaurants)

@home.route('/insert', methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        # Check if the email already exists
        existing_restaurant = Restaurant.query.filter_by(email=email).first()
        if existing_restaurant:
            flash('A restaurant with this email already exists!', 'warning')
            return redirect(url_for('home.listings'))  # Redirect back to the form

        new_restaurant = Restaurant(name=name, location=location, email=email, telephone=telephone)
        
        try:
            db.session.add(new_restaurant)
            db.session.commit()
            flash("Restaurant added successfully!", "success")
        except IntegrityError:
            db.session.rollback() # Rollback the transaction to prevent the database from getting corrupted
            flash("This email is already in use. Please use a different one!", "danger")    
            return redirect(url_for('home.listings'))
    
    return render_template('listingz.html')

@home.route('/update/<int:id>', methods=['POST'])
def update(id):
    restaurant = Restaurant.query.get_or_404(id)  # Get the restaurant by ID

    if request.method == 'POST':
        # Update the restaurant details
        restaurant.name = request.form['name']
        restaurant.location = request.form['location']
        restaurant.email = request.form['email']
        restaurant.telephone = request.form['telephone']

        # Commit changes to the database
        db.session.commit()

        flash("Restaurant updated successfully!", "success")
        return redirect(url_for('home.listings'))

# @home.route('/delete/<int:id>', methods=['POST'])
# def delete(id):
#     restaurant = Restaurant.query.get_or_404(id)  # Get the restaurant by ID

#     # Delete the restaurant
#     db.session.delete(restaurant)
#     db.session.commit()

#     flash("Restaurant deleted successfully!", "success")
#     return redirect(url_for('home.listings'))    
    
@home.route('/guest_listings')
def guest_listings():
    try:
        # only fetch restaurants that are not disabled
        restaurants = Restaurant.query.filter_by(is_disabled=False).all()
        return render_template('guestlistings.html', items=restaurants)   
    except Exception as e: 
        flash(f"Error loading restaurants: {str(e)}", 'danger')
        return redirect(url_for('home.insert'))

# routes ti handle enable and disable buttons
@home.route('/disable/<int:id>', methods=['POST'])
def disable(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        restaurant.is_disabled = True
        db.session.commit()
        flash(f"{restaurant.name} has been disabled.", "warning")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while disabling the restaurant.", "danger")
    return redirect(url_for('home.listings'))

@home.route('/enable/<int:id>', methods=['POST'])
def enable(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        restaurant.is_disabled = False
        db.session.commit()
        flash(f"{restaurant.name} has been enabled.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while enabling the restaurant.", "danger")
    return redirect(url_for('home.listings'))

@home.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        restaurant = Restaurant.query.get_or_404(id)
        if restaurant.is_disabled:
            db.session.delete(restaurant)
            db.session.commit()
            flash(f"{restaurant.name} has been deleted.", "danger")
        else:
            flash("Cannot delete an active restaurant. Please disable it first.", "warning")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the restaurant.", "danger")
    return redirect(url_for('home.listings'))



