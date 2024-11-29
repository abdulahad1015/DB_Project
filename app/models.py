from . import db,bcrypt
from flask_login import UserMixin

class RawMaterial(db.Model):
    __tablename__ = 'raw_material'
    raw_material_id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Matches your schema's primary key
    material_name = db.Column(db.String(100), nullable=False)  # For material_name
    supplier = db.Column(db.String(100), nullable=True)  # For supplier, can be NULL
    quantity_in_stock = db.Column(db.Integer, nullable=False)  # For quantity_in_stock
    import_date = db.Column(db.Date, nullable=True)  # For import_date, can be NULL
    imported = db.Column(db.Boolean, nullable=False, default=False)  # For imported (tinyint)
    semi_finish = db.Column(db.Boolean, nullable=False, default=False)  # For semi_finish (tinyint)

# (Added By Affan)
class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Matches your schema's primary key
    product_name = db.Column(db.String(100), nullable=False)  # For product_name
    category = db.Column(db.String(50), nullable=True)  # For category, can be NULL
    description = db.Column(db.Text, nullable=True)  # For description, can be NULL


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        
        return bcrypt.check_password_hash(self.password_hash, password)