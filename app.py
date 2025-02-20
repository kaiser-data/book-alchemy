import os
from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import sqlalchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')

# Define the database configuration
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'library.sqlite')
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)


def seed_initial_data():
    """Seed the database with initial data if tables are empty."""
    try:
        if not Author.query.first() and not Book.query.first():
            print("Seeding initial data...")

            # Sample authors
            authors_data = [
                {"name": "J.K. Rowling", "birth_date": "1965-07-31"},
                {"name": "George Orwell", "birth_date": "1903-06-25", "date_of_death": "1950-01-21"},
                {"name": "Agatha Christie", "birth_date": "1890-09-15", "date_of_death": "1976-01-12"},
                {"name": "Ernest Hemingway", "birth_date": "1899-07-21", "date_of_death": "1961-07-02"},
                {"name": "Jane Austen", "birth_date": "1775-12-16", "date_of_death": "1817-07-18"}
            ]

            # Convert string dates to Date objects
            for author_data in authors_data:
                author = Author(
                    name=author_data["name"],
                    birth_date=datetime.strptime(author_data["birth_date"], "%Y-%m-%d").date() if author_data.get(
                        "birth_date") else None,
                    date_of_death=datetime.strptime(author_data["date_of_death"], "%Y-%m-%d").date() if author_data.get(
                        "date_of_death") else None
                )
                db.session.add(author)

            db.session.commit()  # Commit authors first to get IDs

            # Sample books
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
                book = Book(**book_data)
                db.session.add(book)

            db.session.commit()

            print("Database initialized successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing database: {e}")


# Set up the database and seed data
with app.app_context():
    db.create_all()
    seed_initial_data()


# Routes
@app.route('/')
def home():
    """Home page route that shows all books with optional sorting."""
    sort_by = request.args.get('sort_by', 'title')

    if sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name.asc()).all()
    else:  # Default to title sorting
        books = Book.query.order_by(Book.title.asc()).all()

    authors = Author.query.order_by(Author.name.asc()).all()
    return render_template('home.html', books=books, authors=authors)


@app.route('/add_author', methods=['POST'])
def add_author():
    """Add a new author to the database."""
    try:
        name = request.form.get('name')
        if not name:
            flash('Author name is required', 'error')
            return redirect(url_for('home'))

        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        # Convert string dates to Date objects
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date() if birth_date else None
        date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d").date() if date_of_death else None

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        flash(f'Author "{name}" added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding author: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.route('/add_book', methods=['POST'])
def add_book():
    """Add a new book to the database."""
    try:
        # Get form data
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        # Validate required fields
        if not all([isbn, title, publication_year, author_id]):
            flash('All fields are required', 'error')
            return redirect(url_for('home'))

        # Create and save the book
        book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year),
            author_id=int(author_id)
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{title}" added successfully', 'success')
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        flash(f'A book with ISBN {isbn} already exists', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding book: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Delete a book from the database."""
    try:
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        flash(f'Book "{book.title}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    """Delete an author and all their books from the database."""
    try:
        author = Author.query.get_or_404(author_id)
        author_name = author.name
        db.session.delete(author)
        db.session.commit()
        flash(f'Author "{author_name}" and all their books deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting author: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))