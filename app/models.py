from . import db

class RawMaterial(db.Model):
    __tablename__ = 'raw_material'
    raw_material_id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Matches your schema's primary key
    material_name = db.Column(db.String(100), nullable=False)  # For material_name
    supplier = db.Column(db.String(100), nullable=True)  # For supplier, can be NULL
    quantity_in_stock = db.Column(db.Integer, nullable=False)  # For quantity_in_stock
    import_date = db.Column(db.Date, nullable=True)  # For import_date, can be NULL
    imported = db.Column(db.Boolean, nullable=False, default=False)  # For imported (tinyint)
    semi_finish = db.Column(db.Boolean, nullable=False, default=False)  # For semi_finish (tinyint)