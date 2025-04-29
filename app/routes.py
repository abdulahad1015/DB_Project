from flask import render_template, redirect, url_for,flash,request,get_flashed_messages,session,abort
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from .forms import *
from . import db
from flask import current_app as app
from .email_otp import send_otp
from functools import wraps
from sqlalchemy.exc import IntegrityError

roles_permissions = {
    "admin": [
        "view_warehouse", "add_warehouse", "edit_warehouse", "delete_warehouse",
        "view_products", "add_product", "edit_product", "delete_product",
        "view_raw_material", "add_raw_material", "edit_raw_material", "delete_raw_material",
        "view_users", "add_user", "edit_user", "delete_user",
        "view_contractors", "edit_contractor", "delete_contractor",
        "view_production_lines", "add_production_line", "edit_production_line", "delete_production_line",
        "view_supervisors", "edit_supervisor", "delete_supervisor",
        "view_product_raw_materials", "add_product_raw_material", "edit_product_raw_material", "delete_product_raw_material",
        "view_production_orders", "add_production_order", "edit_production_order", "delete_production_order",
        "view_material_collections", "add_material_collection", "edit_material_collection", "delete_material_collection",
        "view_finished_goods", "add_finished_goods", "edit_finished_goods", "delete_finished_goods",
        "view_production_report", "add_production_report", "edit_production_report", "delete_production_report",
    
    ],
    "manager": [
        "view_warehouse", "add_warehouse", "edit_warehouse", "delete_warehouse",
        "view_products", "add_product", "edit_product", "delete_product",
        "view_raw_material", "add_raw_material", "edit_raw_material", "delete_raw_material",
        "view_contractors", "edit_contractor", "delete_contractor",
        "view_production_lines", "add_production_line", "edit_production_line", "delete_production_line",
        "view_supervisors", "edit_supervisor", "delete_supervisor",
        "view_product_raw_materials", "add_product_raw_material", "edit_product_raw_material", "delete_product_raw_material",
        "view_production_orders", "add_production_order", "edit_production_order", "delete_production_order",
        "view_material_collections", "add_material_collection", "edit_material_collection", "delete_material_collection",
        "view_finished_goods", "add_finished_goods", "edit_finished_goods", "delete_finished_goods",
    ],
    "staff": [
        "view_warehouse", "view_products", "view_raw_material", "view_contractors",
        "view_production_lines", "view_supervisors", "view_product_raw_materials"
    ],
    "supervisor": [
        "view_products", "view_raw_material", "view_product_raw_materials"
    ],
    "contractor": [
        "view_products", "view_raw_material"
    ]
}


@app.context_processor
def inject_permissions():
    if current_user.is_authenticated:
        return {"username": current_user.username, "user_permissions": roles_permissions.get(current_user.role, [])}
    return {"username": "Guest", "permissions": []}

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in roles:
                return func(*args, **kwargs)
            else:
                abort(403)  # Forbidden
        return wrapper
    return decorator

@app.route('/')
@login_required
def home():
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = SignupForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            if form.role.data == 'contractor':
                contractor = Contractor(user_id=user.id)
                db.session.add(contractor)
                db.session.commit()
            elif form.role.data == 'supervisor':    
                supervisor = Supervisor(supervisor_name=user.username)
                db.session.add(supervisor)
                db.session.commit()
        else:
            flash('Invalid input', 'danger')
            return render_template('signup.html', form=form)

        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    
    session['otp'] = send_otp("k224353@nu.edu.pk")
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))


    form = LoginForm()
    if form.validate_on_submit():
        if form.login.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                from . import session
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Login failed. Check your username and password.', 'danger')
        elif form.forgot_password.data:
            # Implement forgot password functionality here
            flash('Forgot password functionality is not implemented yet.', 'warning')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    from . import session
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    data = {
        "user": "John Doe",
        "total_users": 120,
        "active_users": 85,
        "new_users": 10,
        "recent_activity": ["Added user 'Alice'", "Updated role for 'Bob'"],
    }
    return render_template('dashboard.html', username=current_user.username,data=data)


#---------------------------------------Raw Material----------------------------------------------

# View Raw Material
@app.route('/raw_material')
@login_required
def view_raw_material():
    entries = RawMaterial.query.all()
    print(entries)
    return render_template('raw_material.html', raw_materials=entries)

# Add Raw Material
@app.route('/add_raw_material', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_raw_material():
    form = AddRawMaterialForm()
    if form.validate_on_submit():
        # Create a new instance of RawMaterial with data from the form
        new_material = RawMaterial(
            material_name=form.material_name.data,
            supplier=form.supplier.data,
            quantity_in_stock=form.quantity_in_stock.data,
            import_date=form.import_date.data,
            imported=form.imported.data,
            semi_finish=form.semi_finish.data
        )
        # Add the new material to the database
        db.session.add(new_material)
        db.session.commit()
        flash("Raw material added successfully!", "success")
        return redirect(url_for('view_raw_material'))  # Redirect to the raw materials page
    # Render a specific template for adding raw materials
    return render_template('form.html', form=form)

# Edit Raw Material
@app.route('/edit_raw_material/<int:material_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_raw_material(material_id):
    material = RawMaterial.query.get_or_404(material_id)
    form = AddRawMaterialForm(obj=material)
    if form.validate_on_submit():
        material.material_name=form.material_name.data,
        material.supplier=form.supplier.data,
        material.quantity_in_stock=form.quantity_in_stock.data,
        material.import_date=form.import_date.data,
        material.imported=form.imported.data,
        material.semi_finish=form.semi_finish.data
        db.session.commit()
        flash("Raw material updated successfully!", "success")
        return redirect(url_for('view_raw_material'))
    return render_template('form.html', form=form, material=material)

# Delete Raw Material
@app.route('/delete_raw_material/<int:material_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_raw_material(material_id):
    material = RawMaterial.query.get_or_404(material_id)
    dependencies = ProductRawMaterial.query.filter_by(raw_material_id=material_id).all()
    try:
        db.session.delete(material)
        db.session.commit()
        flash("Raw material deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete raw material: This material is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_raw_material'))


#---------------------------------------Product----------------------------------------------
@app.route('/products')
@login_required
def view_products():
    entries = Product.query.all()  # Fetch all entries from the Product table
    print(entries)  # Debugging: Print entries to console
    return render_template('product.html', products=entries)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            product_name=form.product_name.data,
            category=form.category.data,
            description=form.description.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('view_products'))
    return render_template('form.html', form=form)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.category = form.category.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('view_products'))
    return render_template('form.html', form=form, product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    dependencies = ProductRawMaterial.query.filter_by(product_id=product_id).all()
    if dependencies:
        flash('Cannot delete product. It is currently linked to raw materials.', 'warning')
        return redirect(url_for('view_products'))
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('view_products'))

#---------------------------------------Warehouse----------------------------------------------

@app.route('/warehouse')
@login_required
def view_warehouse():
    entries = Warehouse.query.all()
    print(entries)
    return render_template('warehouse.html', warehouses=entries)

# Add Warehouse
@app.route('/add_warehouse', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_warehouse():
    form = WarehouseForm()
    if form.validate_on_submit():
        new_warehouse = Warehouse(
            warehouse_type=form.warehouse_type.data,
            warehouse_location=form.warehouse_location.data
        )
        db.session.add(new_warehouse)
        db.session.commit()
        flash("Warehouse added successfully!", "success")
        return redirect(url_for('view_warehouse'))
    return render_template('form.html', form=form)

# Edit Warehouse
@app.route('/edit_warehouse/<int:warehouse_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    form = WarehouseForm(obj=warehouse)
    if form.validate_on_submit():
        warehouse.warehouse_type = form.warehouse_type.data
        warehouse.warehouse_location = form.warehouse_location.data
        db.session.commit()
        flash("Warehouse updated successfully!", "success")
        return redirect(url_for('view_warehouse'))
    return render_template('form.html', form=form, warehouse=warehouse)

# Delete Warehouse
@app.route('/delete_warehouse/<int:warehouse_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    try:
        db.session.delete(warehouse)
        db.session.commit()
        flash("Warehouse deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete warehouse: This warehouse is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_warehouse'))

#---------------------------------------User----------------------------------------------
@app.route('/users')
@login_required
def view_users():
    entries = User.query.all()
    print(entries)
    return render_template('user.html', users=entries)

# Add User
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    form = SignupForm()
    form._fields.pop('verification_code')
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if form.role.data == 'contractor':
            contractor = Contractor(user_id=user.id)
            db.session.add(contractor)
            db.session.commit()
        
        if form.role.data == 'supervisor':
            supervisor = Supervisor(supervisor_name=user.username)
            db.session.add(supervisor)
            db.session.commit()

        flash("User added successfully!", "success")
        return redirect(url_for('view_users'))
    return render_template('form.html', form=form)

# Edit User
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    if(user_id == 1):
        flash("Cannot edit the admin user", "danger")
        return redirect(url_for('view_users'))
    user = User.query.get_or_404(user_id)
    form = SignupForm(obj=user)
    # form._fields.pop('password')
    # form._fields.pop('confirm_password')
    form._fields.pop('verification_code')
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('view_users'))
    return render_template('form.html', form=form, user=user)

# Delete User
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    if(user_id == 1):
        flash("Cannot delete the admin user", "danger")
        return redirect(url_for('view_users'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for('view_users'))


#---------------------------------------Contractor----------------------------------------------
@app.route('/contractors')
@login_required
@role_required('admin','manager')
def view_contractors():
    entries = Contractor.query.all()
    print(entries)
    return render_template('contractor.html', contractors=entries)

# Edit Contractor
@app.route('/edit_contractor/<int:contractor_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_contractor(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    form = ContractorForm(obj=contractor)
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        contractor.user_id = contractor_id
        contractor.contract_start_date = form.contract_start_date.data
        contractor.contract_end_date = form.contract_end_date.data
        db.session.commit()
        flash("Contractor updated successfully!", "success")
        return redirect(url_for('view_contractors'))
    return render_template('form.html', form=form, contractor=contractor)

# Delete Contractor
@app.route('/delete_contractor/<int:contractor_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_contractor(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    try:
        db.session.delete(contractor)
        db.session.commit()
        flash("Contractor deleted successfully.", "success")
    except IntegrityError as e:
        db.session.rollback()  # Roll back the transaction to keep the DB in a valid state
        flash("Cannot delete contractor: This contractor is referenced in other records.", "danger")
        # Log the error for debugging (optional)
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_contractors'))


#---------------------------------------Production Line----------------------------------------------

# View Production Line
@app.route('/production_lines')
@login_required
def view_production_lines():
    entries = ProductionLine.query.all()
    print(entries)
    return render_template('production_line.html', production_lines=entries)

# Add Production Line
@app.route('/add_production_line', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_production_line():
    form = ProductionLineForm()
    if form.validate_on_submit():
        new_production_line = ProductionLine(
            line_name=form.line_name.data
        )
        db.session.add(new_production_line)
        db.session.commit()
        flash("Production line added successfully!", "success")
        return redirect(url_for('view_production_lines'))
    return render_template('form.html', form=form)

# Edit Production Line
@app.route('/edit_production_line/<int:production_line_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_production_line(production_line_id):
    production_line = ProductionLine.query.get_or_404(production_line_id)
    form = ProductionLineForm(obj=production_line)
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        production_line.line_name = form.line_name.data
        db.session.commit()
        flash("Production line updated successfully!", "success")
        return redirect(url_for('view_production_lines'))
    return render_template('form.html', form=form, production_line=production_line)

# Delete Production Line
@app.route('/delete_production_line/<int:production_line_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_production_line(production_line_id):
    production_line = ProductionLine.query.get_or_404(production_line_id)
    db.session.delete(production_line)
    db.session.commit()
    flash("Production line deleted successfully!", "success")
    return redirect(url_for('view_production_lines'))

#---------------------------------------Supervisor----------------------------------------------
@app.route('/supervisors')
@login_required
def view_supervisors():
    entries = Supervisor.query.all()
    print(entries)
    return render_template('supervisor.html', supervisors=entries)

# Edit Supervisor
@app.route('/edit_supervisor/<int:supervisor_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_supervisor(supervisor_id):
    supervisor = Supervisor.query.get_or_404(supervisor_id)
    form = SupervisorForm(obj=supervisor)
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        supervisor.supervisor_name = form.supervisor_name.data
        supervisor.contact_info = form.contact_info.data
        supervisor.contractor_id = form.contractor_id.data
        db.session.commit()
        flash("Supervisor updated successfully!", "success")
        return redirect(url_for('view_supervisors'))
    return render_template('form.html', form=form, supervisor=supervisor)

# Delete Supervisor
@app.route('/delete_supervisor/<int:supervisor_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_supervisor(supervisor_id):
    supervisor = Supervisor.query.get_or_404(supervisor_id)
    try:
        db.session.delete(supervisor)
        db.session.commit()
        flash("Supervisor deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete supervisor: This supervisor is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_supervisors'))

#---------------------------------------Product Raw Material----------------------------------------------
@app.route('/product_raw_materials')
@login_required
def view_product_raw_materials():
    entries = ProductRawMaterial.query.all()
    print(entries)
    return render_template('product_raw_material.html', product_raw_materials=entries)

# Add Product Raw Material
@app.route('/add_product_raw_material', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_product_raw_material():
    form = ProductRawMaterialForm()
    if form.validate_on_submit():
        new_product_raw_material = ProductRawMaterial(
            product_id=form.product_id.data,
            raw_material_id=form.raw_material_id.data,
            quantity_required=form.quantity_required.data
        )
        db.session.add(new_product_raw_material)
        db.session.commit()
        flash("Product raw material added successfully!", "success")
        return redirect(url_for('view_product_raw_materials'))
    return render_template('form.html', form=form)

# Edit Product Raw Material
@app.route('/edit_product_raw_material/<int:product_id>/<int:raw_material_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_product_raw_material(product_id, raw_material_id):
    product_raw_material = ProductRawMaterial.query.get_or_404((product_id, raw_material_id))
    form = ProductRawMaterialForm(obj=product_raw_material)
    form.submit.label.text = "Confirm"
    if form.validate_on_submit():
        product_raw_material.product_id = form.product_id.data
        product_raw_material.raw_material_id = form.raw_material_id.data
        product_raw_material.quantity_required = form.quantity_required.data
        db.session.commit()
        flash("Product raw material updated successfully!", "success")
        return redirect(url_for('view_product_raw_materials'))
    return render_template('form.html', form=form, product_raw_material=product_raw_material)

# Delete Product Raw Material
@app.route('/delete_product_raw_material/<int:product_id>/<int:raw_material_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_product_raw_material(product_id, raw_material_id):
    product_raw_material = ProductRawMaterial.query.get_or_404((product_id, raw_material_id))
    try:
        db.session.delete(product_raw_material)
        db.session.commit()
        flash("Product raw material deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete product raw material: This record is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")

    return redirect(url_for('view_product_raw_materials'))

#---------------------------------------Production Order----------------------------------------------

@app.route('/production_orders')
@login_required
@role_required('admin','manager')
def view_production_orders():
    entries = ProductionOrder.query.all()
    print(entries)
    return render_template('production_order.html', production_orders=entries)

# Add Production Order
@app.route('/add_production_order', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_production_order():

    form = ProductionOrderForm()

    unavailable_supervisors = db.session.query(ProductionOrder.supervisor_id).filter_by(status='pending').all()
    unavailable_ids = [s[0] for s in unavailable_supervisors]
    available_supervisors = Supervisor.query.filter(~Supervisor.supervisor_id.in_(unavailable_ids)).all()

    # Dynamically populate the choices
    form.contractor_id.choices = [(c.contractor_id, c.user.username) for c in Contractor.query.all()]
    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    form.production_line_id.choices = [(pl.production_line_id, pl.line_name) for pl in ProductionLine.query.all()]
    form.supervisor.choices = [(s.supervisor_id,s.supervisor_name) for s in available_supervisors]

    if form.validate_on_submit():
        production_order = ProductionOrder(
            contractor_id=form.contractor_id.data,
            product_id=form.product_id.data,
            quantity_ordered=form.quantity_ordered.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            production_line_id=form.production_line_id.data,
            supervisor_id=form.supervisor.data
        )
        db.session.add(production_order)
        db.session.commit()
        return redirect(url_for('view_production_orders'))  # Redirect to a relevant page

    return render_template('form.html', form=form)

# Edit Production Order
@app.route('/edit_production_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_production_order(order_id):
    production_order = ProductionOrder.query.get_or_404(order_id)
    form = ProductionOrderForm(obj=production_order)
    form._fields.pop('supervisor')
    form._fields.pop('contractor_id')

    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    form.production_line_id.choices = [(pl.production_line_id, pl.line_name) for pl in ProductionLine.query.all()]
    if form.validate_on_submit():
        production_order.contractor_id = form.contractor_id.data
        production_order.product_id = form.product_id.data
        production_order.quantity_ordered = form.quantity_ordered.data
        production_order.start_date = form.start_date.data
        production_order.end_date = form.end_date.data
        production_order.production_line_id = form.production_line_id.data
        production_order.supervisor_id = form.supervisor.data
        db.session.commit()
        return redirect(url_for('view_production_orders'))
    return render_template('form.html', form=form, production_order=production_order)

# Delete Production Order
@app.route('/delete_production_order/<int:order_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_production_order(order_id):
    production_order = ProductionOrder.query.get_or_404(order_id)
    
    try:
        db.session.delete(production_order)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete production order: This order is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")

    return redirect(url_for('view_production_orders'))

#---------------------------------------Material Collection----------------------------------------------
@app.route('/material_collections')
@login_required
def view_material_collections():
    entries = MaterialCollection.query.all()
    print(entries)
    return render_template('material_collection.html', material_collections=entries)

# Add Material Collection
@app.route('/add_material_collection', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_material_collection():
    form = MaterialCollectionForm()
    form.supervisor_id.choices = [(s.supervisor_id, s.supervisor_name) for s in Supervisor.query.all()]
    form.raw_material_id.choices = [(r.raw_material_id, r.material_name) for r in RawMaterial.query.all()]
    if form.validate_on_submit():
        new_material_collection = MaterialCollection(
            supervisor_id=form.supervisor_id.data,
            raw_material_id=form.raw_material_id.data,
            quantity_collected=form.quantity_collected.data,
            collection_date=form.collection_date.data
        )
        db.session.add(new_material_collection)
        db.session.commit()
        flash("Material collection added successfully!", "success")
        return redirect(url_for('view_material_collections'))
    return render_template('form.html', form=form)

# Edit Material Collection
@app.route('/edit_material_collection/<int:collection_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_material_collection(collection_id):
    material_collection = MaterialCollection.query.get_or_404(collection_id)
    form = MaterialCollectionForm(obj=material_collection)
    form.supervisor_id.choices = [(s.supervisor_id, s.supervisor_name) for s in Supervisor.query.all()]
    form.raw_material_id.choices = [(r.raw_material_id, r.material_name) for r in RawMaterial.query.all()]
    if form.validate_on_submit():
        material_collection.supervisor_id = form.supervisor_id.data
        material_collection.raw_material_id = form.raw_material_id.data
        material_collection.quantity_collected = form.quantity_collected.data
        material_collection.collection_date = form.collection_date.data
        db.session.commit()
        flash("Material collection updated successfully!", "success")
        return redirect(url_for('view_material_collections'))
    return render_template('form.html', form=form, material_collection=material_collection)

# Delete Material Collection
@app.route('/delete_material_collection/<int:collection_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_material_collection(collection_id):
    material_collection = MaterialCollection.query.get_or_404(collection_id)
    try:
        db.session.delete(material_collection)
        db.session.commit()
        flash("Material collection deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete material collection: This record is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_material_collections'))

#---------------------------------------Finished Goods----------------------------------------------    
@app.route('/finished_goods')
@login_required
def view_finished_goods():
    entries = FinishedGoods.query.all()
    print(entries)
    return render_template('finished_goods.html', finished_goods=entries)

# Add Finished Goods
@app.route('/add_finished_goods', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def add_finished_goods():
    form = FinishedGoodsForm()
    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    form.warehouse_id.choices = [(w.warehouse_id, w.warehouse_location) for w in Warehouse.query.all()]
    if form.validate_on_submit():
        new_finished_goods = FinishedGoods(
            product_id=form.product_id.data,
            quantity_produced=form.quantity_produced.data,
            warehouse_id=form.warehouse_id.data,
            date_stored=form.date_stored.data
        )
        db.session.add(new_finished_goods)
        db.session.commit()
        flash("Finished goods added successfully!", "success")
        return redirect(url_for('view_finished_goods'))
    return render_template('form.html', form=form)

# Edit Finished Goods
@app.route('/edit_finished_goods/<int:finished_goods_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager')
def edit_finished_goods(finished_goods_id):
    finished_goods = FinishedGoods.query.get_or_404(finished_goods_id)
    form = FinishedGoodsForm(obj=finished_goods)
    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    form.warehouse_id.choices = [(w.warehouse_id, w.warehouse_location) for w in Warehouse.query.all()]
    if form.validate_on_submit():
        finished_goods.product_id = form.product_id.data
        finished_goods.quantity_produced = form.quantity_produced.data
        finished_goods.warehouse_id = form.warehouse_id.data
        finished_goods.date_stored = form.date_stored.data
        db.session.commit()
        flash("Finished goods updated successfully!", "success")
        return redirect(url_for('view_finished_goods'))
    return render_template('form.html', form=form, finished_goods=finished_goods)

# Delete Finished Goods
@app.route('/delete_finished_goods/<int:finished_goods_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_finished_goods(finished_goods_id):
    finished_goods = FinishedGoods.query.get_or_404(finished_goods_id)
    try:
        db.session.delete(finished_goods)
        db.session.commit()
        flash("Finished goods deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete finished goods: This record is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_finished_goods'))

#------------------------------------Production_Report----------------------------------------------
@app.route('/production_report')
@login_required
def view_production_report():
    entries = ProductionReport.query.all()
    print(entries)
    return render_template('production_report.html', production_reports=entries)



# Add Production Report
@app.route('/add_production_report', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager','supervisor')
def add_production_report():
    form = ProductionReportForm()
    form.supervisor_id.choices = [(s.supervisor_id, s.supervisor_name) for s in Supervisor.query.all()]
    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    if form.validate_on_submit():
        new_production_report = ProductionReport(
            supervisor_id=form.supervisor_id.data,
            product_id=form.product_id.data,
            quantity_produced=form.quantity_produced.data,
            quantity_faulty=form.quantity_faulty.data,
            parts_issued=form.parts_issued.data,
            report_date=form.report_date.data
        )
        db.session.add(new_production_report)
        db.session.commit()
        flash("Production report added successfully!", "success")
        return redirect(url_for('view_production_report'))
    return render_template('form.html', form=form)

# Edit Production Report
@app.route('/edit_production_report/<int:report_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin','manager','supervisor')
def edit_production_report(report_id):
    production_report = ProductionReport.query.get_or_404(report_id)
    form = ProductionReportForm(obj=production_report)
    form.supervisor_id.choices = [(s.supervisor_id, s.supervisor_name) for s in Supervisor.query.all()]
    form.product_id.choices = [(p.product_id, p.product_name) for p in Product.query.all()]
    if form.validate_on_submit():
        production_report.supervisor_id = form.supervisor_id.data
        production_report.product_id = form.product_id.data
        production_report.quantity_produced = form.quantity_produced.data
        production_report.quantity_faulty = form.quantity_faulty.data
        production_report.parts_issued = form.parts_issued.data
        production_report.report_date = form.report_date.data
        db.session.commit()
        flash("Production report updated successfully!", "success")
        return redirect(url_for('view_production_report'))
    return render_template('form.html', form=form, production_report=production_report)

# Delete Production Report
@app.route('/delete_production_report/<int:report_id>', methods=['POST'])
@login_required
@role_required('admin','manager','supervisor')
def delete_production_report(report_id):
    production_report = ProductionReport.query.get_or_404(report_id)
    try:
        db.session.delete(production_report)
        db.session.commit()
        flash("Production report deleted successfully!", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash("Cannot delete production report: This record is referenced in other records.", "danger")
        app.logger.error(f"IntegrityError: {str(e)}")
    return redirect(url_for('view_production_report'))



#---------------------------------------Profile----------------------------------------------
# @app.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', user=current_user)



#---------------------------------------Error Handling----------------------------------------------
# @app.errorhandler(403)
# def forbidden(e):
#     return render_template('403.html'), 403

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def server_error(e):
#     return render_template('500.html'), 500

#---------------------------------------Miscellaneous----------------------------------------------
