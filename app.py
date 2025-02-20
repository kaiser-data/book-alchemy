from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import requests

app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)

# Seed data if the tables are empty (for initial setup)
with app.app_context():
    if not Author.query.first() or not Book.query.first():
        print("Seeding initial data...")
        # Add sample authors
        authors_data = [
            {"name": "J.K. Rowling", "birth_date": "1965-07-31"},
            {"name": "George Orwell", "birth_date": "1903-06-25", "date_of_death": "1950-01-21"},
            {"name": "Agatha Christie", "birth_date": "1890-09-15", "date_of_death": "1976-01-12"},
            {"name": "Ernest Hemingway", "birth_date": "1899-07-21", "date_of_death": "1961-07-02"},
            {"name": "Jane Austen", "birth_date": "1775-12-16", "date_of_death": "1817-07-18"}
        ]
        for author_data in authors_data:
            author = Author(name=author_data["name"], birth_date=author_data.get("birth_date"),
                            date_of_death=author_data.get("date_of_death"))
            db.session.add(author)

        # Add sample books
        books_data = [
            {"isbn": "9780545010221", "title": "Harry Potter and the Sorcerer's Stone", "publication_year": 1997,
             "author_id": 1},
            {"isbn": "9780451524935", "title": "1984", "publication_year": 1949, "author_id": 2},
            {"isbn": "9780062073480", "title": "Murder on the Orient Express", "publication_year": 1934,
             "author_id": 3},
            {"isbn": "9780684801223", "title": "The Old Man and the Sea", "publication_year": 1952, "author_id": 4},
            {"isbn": "9780141439518", "title": "Pride and Prejudice", "publication_year": 1813, "author_id": 5}
        ]
        for book_data in books_data:
            book = Book(isbn=book_data["isbn"], title=book_data["title"],
                        publication_year=book_data["publication_year"], author_id=book_data["author_id"])
            db.session.add(book)
        db.session.commit()


# Home page route
@app.route('/', methods=['GET'])
def home():
    sort_by = request.args.get('sort_by', 'title')  # Default sorting by title
    if sort_by == 'title':
        books = Book.query.order_by(Book.title.asc()).all()
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name.asc()).all()
    else:
        books = Book.query.all()

    return render_template('home.html', books=books)


# Route to add an author
@app.route('/add_author', methods=['POST'])
def add_author():
    name = request.form.get('name')
    birth_date = request.form.get('birth_date')
    date_of_death = request.form.get('date_of_death')
    author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
    db.session.add(author)
    db.session.commit()
    return redirect(url_for('home'))


# Route to add a book
@app.route('/add_book', methods=['POST'])
def add_book():
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    publication_year = request.form.get('publication_year')
    author_id = request.form.get('author_id')
    book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)