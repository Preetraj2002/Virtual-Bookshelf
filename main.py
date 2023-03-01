from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

all_books = []
#
# class BookForm():
#     title=StringField("Title",validators=[DataRequired()])
#     author=StringField("Author",validators=[DataRequired()])
#     rating=IntegerField("Rating (??/10)",validators=[DataRequired()])
#



##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    # this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    #     form=BookForm()
    #     if form.
    if request.method == "POST":
        # if request.
        book_dict = request.form.to_dict()
        print(book_dict)
        new_book = Book(title=book_dict['title'], author=book_dict['author'], rating=book_dict['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit",methods=["GET","POST"])
def edit():

    book_id = request.args.get('id')    #taking the id arguement
    # print(book_id)
    # get the book
    book_to_update = Book.query.get(book_id)
    if request.method == "POST":
        book_to_update.rating = request.form['rating']          #change the rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",id=book_id,title=book_to_update.title,rating=book_to_update.rating)


@app.route("/delete")
def delete():
    book_id=request.args.get("id")
    book_to_delete=Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
