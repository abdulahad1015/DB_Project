import os

class Config:
    # Use environment variable to set the DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://root:rootpassword@mysql-db:3306/factory_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'