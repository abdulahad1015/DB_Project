from flask import render_template, redirect, url_for,flash,request,get_flashed_messages,session,abort
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from .forms import *
from . import db
from flask import current_app as app
from .email_otp import send_otp
from functools import wraps

# Decorator to check if the user is logged in and has the required role
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
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        else:
            flash('Invalid input', 'danger')
            return render_template('signup.html', form=form)

        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    
    session['otp'] = send_otp()
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
        "roles": {"Admin": 5, "Editor": 15, "Viewer": 100},
        "recent_activity": ["Added user 'Alice'", "Updated role for 'Bob'"],
    }
    return render_template('dashboard.html', username=current_user.username,data=data)

@app.route('/raw_material')
@login_required
def view_raw_material():
    entries = RawMaterial.query.all()
    print(entries)
    return render_template('raw_material.html', raw_materials=entries)

#---------------------------------------Raw Material----------------------------------------------
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
        material.name = form.name.data
        material.description = form.description.data
        material.quantity = form.quantity.data
        material.cost = form.cost.data
        db.session.commit()
        flash("Raw material updated successfully!", "success")
        return redirect(url_for('home'))
    return render_template('form.html', form=form, material=material)

# Delete Raw Material
@app.route('/delete_raw_material/<int:material_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_raw_material(material_id):
    material = RawMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash("Raw material deleted successfully!", "success")
    return redirect(url_for('home'))


#---------------------------------------Product----------------------------------------------
# (Added By Affan)
@app.route('/products')
@login_required
def view_products():
    entries = Product.query.all()  # Fetch all entries from the Product table
    print(entries)  # Debugging: Print entries to console
    return render_template('product.html', products=entries)

# Add Product (Added By Affan)
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

# Edit Product(Added By Affan)
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

# Delete Product (Added By Affan)
@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
@role_required('admin','manager')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
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
    db.session.delete(warehouse)
    db.session.commit()
    flash("Warehouse deleted successfully!", "success")
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
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User added successfully!", "success")
        return redirect(url_for('view_users'))
    return render_template('form.html', form=form)

# Edit User
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = SignupForm(obj=user)
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for('view_users'))

#---------------------------------------Error Handling----------------------------------------------
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

#---------------------------------------Miscellaneous----------------------------------------------
