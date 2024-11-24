from flask import render_template, redirect, url_for,flash
# from . import create_app
from .models import RawMaterial
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