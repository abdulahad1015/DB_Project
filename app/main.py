# from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FloatField, TextAreaField, SelectField
# from wtforms.fields.numeric import IntegerField
# from wtforms.fields.simple import BooleanField, PasswordField
# from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo
# from datetime import datetime
# from flask_migrate import Migrate
# from flask_bootstrap import Bootstrap5
# from forms import *
# from models import *
# from routes import *
#
#
#
# # Flask app setup
# # set FLASK_APP=main.py
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1:3306/factory_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Bootstrap5(app)
# db = SQLAlchemy(app)
# # migrate = Migrate(app,db)
#
#
# # Models
#
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#
# # Routes
#
#
# # Register
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         new_user = User(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data  # Hash in production
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Registration successful!", "success")
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)
#
# # Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.password == form.password.data:  # Verify password in production
#             flash("Login successful!", "success")
#             return redirect(url_for('index'))
#         flash("Invalid credentials. Please try again.", "danger")
#     return render_template('login.html', form=form)
#
# # Run App
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
