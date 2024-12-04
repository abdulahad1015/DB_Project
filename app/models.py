from . import db,bcrypt
from flask_login import UserMixin

class RawMaterial(db.Model):
    __tablename__ = 'raw_material'
    raw_material_id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # Matches your schema's primary key
    material_name = db.Column(db.String(100), nullable=False)  # For material_name
    supplier = db.Column(db.String(100), nullable=True)  # For supplier, can be NULL
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
    role = db.Column(db.String(50), nullable=False, default='user')
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        
        return bcrypt.check_password_hash(self.password_hash, password)
    
class Warehouse(db.Model):
    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    warehouse_type = db.Column(db.String(50), nullable=False)
    warehouse_location = db.Column(db.String(100), nullable=False)

class Contractor(db.Model):
    contractor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    contract_start_date = db.Column(db.Date, nullable=True)
    contract_end_date = db.Column(db.Date, nullable=True)

    # Relationship to the User table
    user = db.relationship('User', backref=db.backref('contractor', uselist=False), lazy='joined')

class ProductionLine(db.Model):
    production_line_id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(50), nullable=False)

class Supervisor(db.Model):

    supervisor_id = db.Column(db.Integer, primary_key=True)
    supervisor_name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.contractor_id'), nullable=True)

    # Relationship
    contractor = db.relationship('Contractor', backref='supervisors')

class ProductRawMaterial(db.Model):

    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)
    raw_material_id = db.Column(db.Integer, db.ForeignKey('raw_material.raw_material_id'), primary_key=True)
    quantity_required = db.Column(db.Integer, nullable=False)

    # Relationship with Product and RawMaterial
    product = db.relationship('Product', backref=db.backref('product_raw_materials', lazy='joined'))
    raw_material = db.relationship('RawMaterial', backref=db.backref('product_raw_materials', lazy='joined'))



class ProductionOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.contractor_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity_ordered = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    production_line_id = db.Column(db.Integer, db.ForeignKey('production_line.production_line_id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')

    # Relationships for easier navigation
    contractor = db.relationship('Contractor', backref='production_orders', lazy='joined')
    product = db.relationship('Product', backref='production_orders', lazy='joined')
    production_line = db.relationship('ProductionLine', backref='production_orders', lazy='joined')
    supervisor = db.relationship('Supervisor', backref='production_orders', lazy='joined')

class MaterialCollection(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=False)
    raw_material_id = db.Column(db.Integer, db.ForeignKey('raw_material.raw_material_id'), nullable=False)
    quantity_collected = db.Column(db.Integer, nullable=False)
    collection_date = db.Column(db.Date)

    # Relationships (optional)
    supervisor = db.relationship('Supervisor', backref='material_collections',lazy='joined')
    raw_material = db.relationship('RawMaterial', backref='material_collections',lazy='joined')


class FinishedGoods(db.Model):
    finished_goods_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.warehouse_id'), nullable=False)
    date_stored = db.Column(db.Date, nullable=True)

    # Relationships
    product = db.relationship('Product', backref='finished_goods')
    # warehouse = db.relationship('Warehouse', backref='finished_goods')

class ProductionReport(db.Model):

    report_id = db.Column(db.Integer, primary_key=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.supervisor_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity_produced = db.Column(db.Integer, nullable=False)
    quantity_faulty = db.Column(db.Integer, nullable=True)
    parts_issued = db.Column(db.Text, nullable=True)
    report_date = db.Column(db.Date, nullable=True)

    supervisor = db.relationship('Supervisor', backref='reports')
    product = db.relationship('Product', backref='reports')