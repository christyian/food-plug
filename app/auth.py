import datetime
from flask import Blueprint, render_template, request, url_for, flash, redirect
from app.extentions import db
from .models import User
from werkzeug.security import generate_password_hash
import re
from flask_login import login_user, logout_user, login_required

#create the auth blue print
auth = Blueprint('auth', __name__)

#regex username and email
email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
username_regex = r'^[a-zA-Z0-9]+$'
#regex username and email ended here

@auth.route('/signup', methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validate form fields
        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.signup_page"))
        
        #validate email and username
         # Validate email format using regex
        if not re.match(email_regex, email):
            flash("Invalid email format.", "danger")
            return redirect(url_for("auth.signup_page"))

        # Validate username format (only alphanumeric, no spaces or special characters)
        if not re.match(username_regex, username):
            flash("Username can only contain letters and numbers, with no spaces or special characters.", "danger")
            return redirect(url_for("auth.signup_page"))
        #validate ended here

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("auth.signup_page"))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email is already registered", "danger")
            return redirect(url_for("auth.signup_page")) 

        # Create new user
        new_user = User(username=username, email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.log_in"))
    
    return render_template('signup.html')


@auth.route('/login', methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user  = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!,", "success")
            return redirect(url_for("home.profile"))
        else:
            flash("invalid email or password", "danger")
            return redirect(url_for("auth.log_in"))
    
    return render_template("log_in.html")  


@auth.route('/logout')
@login_required  # Ensures only logged-in users can access this route
def log_out():
    logout_user()  # Logs out the current user
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.log_in")) 

