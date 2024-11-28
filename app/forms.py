from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import datetime



# Models
# class RawMaterial(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500))
#     quantity = db.Column(db.Float, nullable=False)
#     cost = db.Column(db.Float, nullable=False)
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

# Forms
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
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

# Add/Update Product (Added by Affan)
class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Add/Update Product")

# # Routes
# @app.route('/')
# def index():
#     raw_materials = RawMaterial.query.all()
#     return render_template('index.html', raw_materials=raw_materials)
#
# # Add Raw Material
# @app.route('/add_raw_material', methods=['GET', 'POST'])
# def add_raw_material():
#     form = AddRawMaterialForm()
#     if form.validate_on_submit():
#         new_material = RawMaterial(
#             name=form.name.data,
#             description=form.description.data,
#             quantity=form.quantity.data,
#             cost=form.cost.data
#         )
#         db.session.add(new_material)
#         db.session.commit()
#         flash("Raw material added successfully!", "success")
#         return redirect(url_for('index'))
#     return render_template('add_raw_material.html', form=form)
#
# # Edit Raw Material
# @app.route('/edit_raw_material/<int:material_id>', methods=['GET', 'POST'])
# def edit_raw_material(material_id):
#     material = RawMaterial.query.get_or_404(material_id)
#     form = AddRawMaterialForm(obj=material)
#     if form.validate_on_submit():
#         material.name = form.name.data
#         material.description = form.description.data
#         material.quantity = form.quantity.data
#         material.cost = form.cost.data
#         db.session.commit()
#         flash("Raw material updated successfully!", "success")
#         return redirect(url_for('index'))
#     return render_template('edit_raw_material.html', form=form, material=material)
#
# # Delete Raw Material
# @app.route('/delete_raw_material/<int:material_id>', methods=['POST'])
# def delete_raw_material(material_id):
#     material = RawMaterial.query.get_or_404(material_id)
#     db.session.delete(material)
#     db.session.commit()
#     flash("Raw material deleted successfully!", "success")
#     return redirect(url_for('index'))

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





# class AddRawMaterialForm(FlaskForm):
#     name = StringField("Material Name", validators=[DataRequired(), Length(max=100)])
#     description = TextAreaField("Description", validators=[DataRequired(), Length(max=500)])
#     quantity = FloatField("Quantity (kg/liters/etc.)", validators=[DataRequired(), NumberRange(min=0)])
#     cost = FloatField("Cost per Unit", validators=[DataRequired(), NumberRange(min=0)])
#     submit = SubmitField("Add Material")


class EditRawMaterialForm(FlaskForm):
    name = StringField("Material Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    quantity = FloatField("Quantity (kg/liters/etc.)", validators=[NumberRange(min=0)])
    cost = FloatField("Cost per Unit", validators=[NumberRange(min=0)])
    submit = SubmitField("Update Material")


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Search")


class DeleteConfirmationForm(FlaskForm):
    confirm = SubmitField("Confirm Deletion")
    cancel = SubmitField("Cancel")


class RateItemForm(FlaskForm):
    rating = FloatField("Rating (1-10)", validators=[DataRequired(), NumberRange(min=1, max=10)])
    review = TextAreaField("Review", validators=[Length(max=500)])
    submit = SubmitField("Submit Rating")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    password = StringField("Password", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Length(max=100)])
    password = StringField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = StringField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

# Add/Edit/Delete Contractor
class AddContractorForm(FlaskForm):
    contractor_name = StringField("Contractor Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add Contractor")

class EditContractorForm(FlaskForm):
    contractor_name = StringField("Contractor Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Update Contractor")

# Add/Edit/Delete Finished Goods
class AddFinishedGoodsForm(FlaskForm):
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity_produced = IntegerField("Quantity Produced", validators=[DataRequired(), NumberRange(min=0)])
    warehouse_id = IntegerField("Warehouse ID", validators=[DataRequired()])
    date_stored = DateField("Date Stored", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Add Finished Goods")

# Add/Edit/Delete Material Collection
class AddMaterialCollectionForm(FlaskForm):
    supervisor_id = IntegerField("Supervisor ID", validators=[DataRequired()])
    raw_material_id = IntegerField("Raw Material ID", validators=[DataRequired()])
    quantity_collected = IntegerField("Quantity Collected", validators=[DataRequired(), NumberRange(min=0)])
    collection_date = DateField("Collection Date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Add Collection")

# Add/Edit/Delete Production Order
class AddProductionOrderForm(FlaskForm):
    contractor_id = IntegerField("Contractor ID", validators=[DataRequired()])
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity_ordered = IntegerField("Quantity Ordered", validators=[DataRequired(), NumberRange(min=1)])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField("End Date", format='%Y-%m-%d')
    production_line_id = IntegerField("Production Line ID", validators=[DataRequired()])
    submit = SubmitField("Add Order")

# Add/Edit/Delete Production Report
class AddProductionReportForm(FlaskForm):
    supervisor_id = IntegerField("Supervisor ID", validators=[DataRequired()])
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity_produced = IntegerField("Quantity Produced", validators=[DataRequired(), NumberRange(min=0)])
    quantity_faulty = IntegerField("Faulty Quantity", validators=[NumberRange(min=0)])
    parts_issued = TextAreaField("Parts Issued")
    report_date = DateField("Report Date", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("Add Report")

# Add/Edit/Delete Supervisor
class AddSupervisorForm(FlaskForm):
    supervisor_name = StringField("Supervisor Name", validators=[DataRequired(), Length(max=100)])
    contact_info = StringField("Contact Info", validators=[Length(max=100)])
    contractor_id = IntegerField("Contractor ID")
    assigned_line = IntegerField("Assigned Line")
    submit = SubmitField("Add Supervisor")

# Add/Edit/Delete Warehouse
class AddWarehouseForm(FlaskForm):
    warehouse_type = StringField("Warehouse Type", validators=[DataRequired(), Length(max=50)])
    warehouse_location = StringField("Warehouse Location", validators=[Length(max=100)])
    submit = SubmitField("Add Warehouse")

# Add/Edit/Delete Product-Raw Material Relationship
class AddProductRawMaterialForm(FlaskForm):
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    raw_material_id = IntegerField("Raw Material ID", validators=[DataRequired()])
    quantity_required = IntegerField("Quantity Required", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add Requirement")

# Search/Filter Forms
class SearchRawMaterialForm(FlaskForm):
    query = StringField("Search Raw Material", validators=[DataRequired()])
    submit = SubmitField("Search")

class SearchProductForm(FlaskForm):
    query = StringField("Search Product", validators=[DataRequired()])
    submit = SubmitField("Search")