from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField,TextAreaField
from wtforms.validators import DataRequired
import requests
import forms

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/movies_db'
Bootstrap5(app)
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# CREATE DB
# class movie(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), unique=True)
#     description: Mapped[str] = mapped_column(String(250), nullable=False)
#     rating: Mapped[float] = mapped_column(Float, nullable=True)
#     ranking: Mapped[int] = mapped_column(Integer, nullable=False)
#     review: Mapped[str] = mapped_column(String(100), nullable=True)
#     img_url: Mapped[str] = mapped_column(String(200), nullable=False)

# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    form = forms.AddRawMaterial()
    # with app.app_context():
    #     result = db.session.execute(db.select(movie).order_by(-movie.rating))
    #     movies = result.scalars().all()
    return render_template("index.html",form=form)

# @app.route("/edit", methods=['GET', 'POST'])
# def edit():
#     num = request.args.get('num', type=int)
#     title = request.args.get('title',type=str)
#
#     form = RateMovieForm()
#     if form.validate_on_submit():
#         data = request.form.to_dict()
#         print("Form submitted and validated")
#         with app.app_context():
#             if num:
#                 result = db.session.execute(db.select(movie).where(movie.id == num))
#             elif title:
#                 result = db.session.execute(db.select(movie).where(movie.title == title))
#             result = result.scalar()
#             result.rating = data['rating']
#             result.review = data['review']
#             db.session.commit()
#
#
#         return redirect(url_for("home"))
#     else:
#         print("Form not validated or wrong method")
#     return render_template("edit.html", form=form)
#
# @app.route("/add", methods=['GET', 'POST'])
# def add():
#     global movies
#     id = request.args.get('id', type=int)
#     if id:
#         for i in movies:
#             if i['id']==id:
#                 print(i['id'])
#                 new=movie(title=i['title'],description=i['overview'],rating=0.0,ranking=0,review=" ",img_url=i['poster_path'])
#                 with app.app_context():
#                     db.session.add(new)
#                     db.session.commit()
#                     return redirect((url_for("edit",title=i['title'])))
#
#     form = AddMovieForm()
#     if form.validate_on_submit():
#         data = request.form.to_dict()
#         name=data['name']
#
#         url = f"https://api.themoviedb.org/3/search/movie?query={name}&api_key=f79377b7e617a7bedc2c81b63d391e21&language=en-US&page=1"
#         headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer f79377b7e617a7bedc2c81b63d391e21"
#         }
#         response = requests.get(url, headers=headers)
#         movies=response.json()['results']
#
#         return render_template("list.html", movies=movies)
#     return render_template("add.html", form=form)
#
#
# @app.route("/delete", methods=['GET', 'POST'])
# def delete():
#     num = request.args.get('num', type=int)
#     with app.app_context():
#         print(num)
#         result = db.session.execute(db.select(movie).where(movie.id == num))
#         result = result.scalar()
#         db.session.delete(result)
#         db.session.commit()
#     return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
