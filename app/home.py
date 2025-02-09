from flask import Blueprint, render_template, url_for, request, redirect, flash
from .models import Restaurant
from app.extentions import db  # import the database instance
from flask_login import login_required, current_user

#create the home blue print
home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    return render_template('index.html')

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

        new_restaurant = Restaurant(name=name, location=location, email=email, telephone=telephone)
        db.session.add(new_restaurant)
        db.session.commit()

        flash("Restaurant added successfully!", "success")
        return redirect(url_for('home.listings'))

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


