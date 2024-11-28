from flask import render_template, redirect, url_for,flash
# from . import create_app
from .models import RawMaterial, Product
from .forms import *
from . import db
from flask import current_app as app


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/raw_material')
def view_raw_material():
    entries = RawMaterial.query.all()
    print(entries)
    return render_template('entries.html', raw_materials=entries)

# (Added By Affan)
@app.route('/products')
def view_products():
    entries = Product.query.all()  # Fetch all entries from the Product table
    print(entries)  # Debugging: Print entries to console
    return render_template('products.html', products=entries)


# Add Raw Material
@app.route('/add_raw_material', methods=['GET', 'POST'])
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
    return render_template('index.html', form=form)

# Edit Raw Material
@app.route('/edit_raw_material/<int:material_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('index.html', form=form, material=material)

# Delete Raw Material
@app.route('/delete_raw_material/<int:material_id>', methods=['POST'])
def delete_raw_material(material_id):
    material = RawMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash("Raw material deleted successfully!", "success")
    return redirect(url_for('index'))

# Add Product (Added By Affan)
@app.route('/add_product', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

# Edit Product(Added By Affan)
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.category = form.category.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_product.html', form=form, product=product)

# Delete Product (Added By Affan)
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('index'))
