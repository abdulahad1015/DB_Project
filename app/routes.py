from flask import render_template, redirect, url_for,flash,session,request,get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from .models import RawMaterial, Product
from .forms import *
from . import db
from flask import current_app as app
from .email_otp import send_otp

otp=None

@app.route('/')
def home():
    return redirect(url_for('login'))

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
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('base.html', username=current_user.username)


@app.route('/raw_material')
@login_required
def view_raw_material():
    entries = RawMaterial.query.all()
    print(entries)
    return render_template('raw_material.html', raw_materials=entries)

# Add Raw Material
@app.route('/add_raw_material', methods=['GET', 'POST'])
@login_required
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
def delete_raw_material(material_id):
    material = RawMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash("Raw material deleted successfully!", "success")
    return redirect(url_for('home'))

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
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('view_products'))
