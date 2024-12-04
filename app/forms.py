from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Email
from wtforms.validators import *
from datetime import datetime
from .models import *

class AddRawMaterialForm(FlaskForm):
    material_name = StringField("Material Name")
    supplier = StringField("Supplier")
    quantity_in_stock = IntegerField("Quantity in Stock")
    import_date = DateField("Import Date")
    imported = BooleanField("Imported")
    semi_finish = BooleanField("Semi-Finished")
    submit = SubmitField("Add Material")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=50)])
    login = SubmitField("         Login        ")
    forgot_password = SubmitField("Forgot Password")

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    role = SelectField('Role', choices=[('manager', 'Manager'), ('contractor', 'Contractor'),('supervisor','Supervisor')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    verification_code = IntegerField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')
        
    def validate_verification_code(self,verification_code):
         # Example of retrieving OTP from the session
        print(f"Verrification code{verification_code.data}")
        from app.routes import session
        otp=int(session['otp'])
        print(f"OTP{otp}")
        if otp is None or int(verification_code.data) != otp:
            raise ValidationError('Invalid OTP.')
# Add/Update Product (Added by Affan)
class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Add/Update Product")

class EditRawMaterialForm(FlaskForm):
    name = StringField("Material Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    quantity = FloatField("Quantity (kg/liters/etc.)", validators=[NumberRange(min=0)])
    cost = FloatField("Cost per Unit", validators=[NumberRange(min=0)])
    submit = SubmitField("Update Material")

class WarehouseForm(FlaskForm):
    warehouse_type = SelectField('Warehouse Type', choices=[('Raw Material', 'Raw Material'), ('Finished Goods', 'Finished Goods')], validators=[DataRequired()])
    warehouse_location = StringField('Warehouse Location', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Warehouse')

class ContractorForm(FlaskForm):
    # user_id = IntegerField("User ID", validators=[DataRequired()])
    contract_start_date = DateField("Contract Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    contract_end_date = DateField("Contract End Date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Add Contractor")

class ProductionLineForm(FlaskForm):
    line_name = StringField("Line Name", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Add Production Line")

class SupervisorForm(FlaskForm):
    supervisor_name = StringField("Supervisor Name", validators=[DataRequired(), Length(max=100)])
    contact_info = StringField("Contact Info", validators=[Length(max=100)])
    contractor_id = IntegerField("Contractor ID", validators=[DataRequired()])
    submit = SubmitField("Add Supervisor")

class ProductRawMaterialForm(FlaskForm):
    product_choices = [(product.product_id, product.product_name) for product in Product.query.all()]
    raw_material_choices = [(raw_material.raw_material_id, raw_material.material_name) for raw_material in RawMaterial.query.all()]
    
    product_id = SelectField('Product', coerce=int, choices=product_choices, validators=[DataRequired()])
    raw_material_id = SelectField('Raw Material', coerce=int, choices=raw_material_choices, validators=[DataRequired()])
    quantity_required = IntegerField('Quantity Required', validators=[DataRequired()])
    
    submit = SubmitField('Save')

class ProductionOrderForm(FlaskForm):

    contractor_id = SelectField('Contractor',coerce=int,validators=[DataRequired()],choices=[] )
    product_id = SelectField('Product',coerce=int,validators=[DataRequired()],choices=[])
    quantity_ordered = IntegerField('Quantity Ordered',validators=[DataRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    production_line_id = SelectField('Production Line',coerce=int,validators=[DataRequired()],choices=[]  )
    supervisor = SelectField('Supervisor',validators=[DataRequired()],choices=[])
    status = SelectField('Status',choices=[('Pending','Pending'),('Completed','Completed')],validators=[DataRequired()])
    submit = SubmitField('Submit')

class MaterialCollectionForm(FlaskForm):
    supervisor_id = SelectField('Supervisor',coerce=int,validators=[DataRequired()],choices=[])
    raw_material_id = SelectField('Raw Material',coerce=int,validators=[DataRequired()],choices=[])
    quantity_collected = IntegerField('Quantity Collected',validators=[DataRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    collection_date = DateField('Collection Date', validators=[DataRequired()])
    submit = SubmitField('Submit')



# class SearchForm(FlaskForm):
#     query = StringField("Search", validators=[DataRequired(), Length(max=100)])
#     submit = SubmitField("Search")


# class DeleteConfirmationForm(FlaskForm):
#     confirm = SubmitField("Confirm Deletion")
#     cancel = SubmitField("Cancel")


# class RateItemForm(FlaskForm):
#     rating = FloatField("Rating (1-10)", validators=[DataRequired(), NumberRange(min=1, max=10)])
#     review = TextAreaField("Review", validators=[Length(max=500)])
#     submit = SubmitField("Submit Rating")


# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), Length(max=50)])
#     password = StringField("Password", validators=[DataRequired(), Length(max=50)])
#     submit = SubmitField("Login")


# class RegisterForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), Length(max=50)])
#     email = StringField("Email", validators=[DataRequired(), Length(max=100)])
#     password = StringField("Password", validators=[DataRequired(), Length(min=6)])
#     confirm_password = StringField("Confirm Password", validators=[DataRequired()])
#     submit = SubmitField("Register")

# Add/Edit/Delete Contractor
# class AddContractorForm(FlaskForm):
#     contractor_name = StringField("Contractor Name", validators=[DataRequired(), Length(max=100)])
#     submit = SubmitField("Add Contractor")

# class EditContractorForm(FlaskForm):
#     contractor_name = StringField("Contractor Name", validators=[DataRequired(), Length(max=100)])
#     submit = SubmitField("Update Contractor")

# # Add/Edit/Delete Finished Goods
# class AddFinishedGoodsForm(FlaskForm):
#     product_id = IntegerField("Product ID", validators=[DataRequired()])
#     quantity_produced = IntegerField("Quantity Produced", validators=[DataRequired(), NumberRange(min=0)])
#     warehouse_id = IntegerField("Warehouse ID", validators=[DataRequired()])
#     date_stored = DateField("Date Stored", format='%Y-%m-%d', validators=[DataRequired()])
#     submit = SubmitField("Add Finished Goods")

# # Add/Edit/Delete Material Collection
# class AddMaterialCollectionForm(FlaskForm):
#     supervisor_id = IntegerField("Supervisor ID", validators=[DataRequired()])
#     raw_material_id = IntegerField("Raw Material ID", validators=[DataRequired()])
#     quantity_collected = IntegerField("Quantity Collected", validators=[DataRequired(), NumberRange(min=0)])
#     collection_date = DateField("Collection Date", format='%Y-%m-%d', validators=[DataRequired()])
#     submit = SubmitField("Add Collection")

# # Add/Edit/Delete Production Order
# class AddProductionOrderForm(FlaskForm):
#     contractor_id = IntegerField("Contractor ID", validators=[DataRequired()])
#     product_id = IntegerField("Product ID", validators=[DataRequired()])
#     quantity_ordered = IntegerField("Quantity Ordered", validators=[DataRequired(), NumberRange(min=1)])
#     start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
#     end_date = DateField("End Date", format='%Y-%m-%d')
#     production_line_id = IntegerField("Production Line ID", validators=[DataRequired()])
#     submit = SubmitField("Add Order")

# # Add/Edit/Delete Production Report
# class AddProductionReportForm(FlaskForm):
#     supervisor_id = IntegerField("Supervisor ID", validators=[DataRequired()])
#     product_id = IntegerField("Product ID", validators=[DataRequired()])
#     quantity_produced = IntegerField("Quantity Produced", validators=[DataRequired(), NumberRange(min=0)])
#     quantity_faulty = IntegerField("Faulty Quantity", validators=[NumberRange(min=0)])
#     parts_issued = TextAreaField("Parts Issued")
#     report_date = DateField("Report Date", format='%Y-%m-%d', validators=[DataRequired()])
#     submit = SubmitField("Add Report")

# # Add/Edit/Delete Supervisor
# class AddSupervisorForm(FlaskForm):
#     supervisor_name = StringField("Supervisor Name", validators=[DataRequired(), Length(max=100)])
#     contact_info = StringField("Contact Info", validators=[Length(max=100)])
#     contractor_id = IntegerField("Contractor ID")
#     assigned_line = IntegerField("Assigned Line")
#     submit = SubmitField("Add Supervisor")

# # Add/Edit/Delete Warehouse
# class AddWarehouseForm(FlaskForm):
#     warehouse_type = StringField("Warehouse Type", validators=[DataRequired(), Length(max=50)])
#     warehouse_location = StringField("Warehouse Location", validators=[Length(max=100)])
#     submit = SubmitField("Add Warehouse")

# # # Add/Edit/Delete Product-Raw Material Relationship
# # class AddProductRawMaterialForm(FlaskForm):
# #     product_id = IntegerField("Product ID", validators=[DataRequired()])
# #     raw_material_id = IntegerField("Raw Material ID", validators=[DataRequired()])
# #     quantity_required = IntegerField("Quantity Required", validators=[DataRequired(), NumberRange(min=1)])
# #     submit = SubmitField("Add Requirement")

# # Search/Filter Forms
# class SearchRawMaterialForm(FlaskForm):
#     query = StringField("Search Raw Material", validators=[DataRequired()])
#     submit = SubmitField("Search")

# class SearchProductForm(FlaskForm):
#     query = StringField("Search Product", validators=[DataRequired()])
#     submit = SubmitField("Search")