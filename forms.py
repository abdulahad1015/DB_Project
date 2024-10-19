from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField,TextAreaField,SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired

class AddRawMaterial(FlaskForm):
    material_name = StringField(label='Material Name', validators=[DataRequired()])
    supplier = StringField(label='Supplier Name', validators=[DataRequired()])
    quantity_in_stock = IntegerField(label='Quantity In Stock', validators=[DataRequired()])
    imported = SelectField('Manufacturing', choices=['Imported','Locally'])
    semi_finish = SelectField('Finishing', choices=['Raw','Semi-Finished'])

class Products(FlaskForm):
    product_name = StringField(label='Product Name', validators=[DataRequired()])
    category = StringField(label='Category', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])

class Contractor(FlaskForm):
    contractor_name = StringField(label='Contractor Name', validators=[DataRequired()])

class Warehouse(FlaskForm):
    warehouse_name = StringField(label='Warehouse Name', validators=[DataRequired()])
    warehouse_location = StringField(label='Warehouse Location', validators=[DataRequired()])