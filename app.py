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

# Ensure tables are created
with app.app_context():
    db.create_all()


# Routes
@app.route('/', methods=['GET'])
def home():
    """Home page route that shows all books with optional sorting and keyword search."""
    sort_by = request.args.get('sort_by', 'title')  # Default sorting by title
    search_query = request.args.get('search', '').strip()  # Get the search query

    if search_query:
        # Perform a case-insensitive search for the keyword in the title or author name
        books = Book.query.filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        ).join(Author).all()
    else:
        # Sort books based on the selected option
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name.asc()).all()
        else:  # Default to title sorting
            books = Book.query.order_by(Book.title.asc()).all()

    authors = Author.query.order_by(Author.name.asc()).all()
    return render_template('home.html', books=books, authors=authors, search_query=search_query)


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
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        # Validate required fields
        if not all([isbn, title, publication_year, author_id]):
            flash('All fields are required', 'error')
            return redirect(url_for('home'))

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


# Delete a book
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    try:
        # Find the book by ID
        book = Book.query.get_or_404(book_id)

        # Delete the book
        db.session.delete(book)
        db.session.commit()

        # Check if the author has any other books left
        author = Author.query.get(book.author_id)
        if author and not author.books:
            # Delete the author if they have no books
            db.session.delete(author)
            db.session.commit()
            flash(f'Author "{author.name}" was also deleted as they had no remaining books.', 'success')

        flash(f'Book "{book.title}" deleted successfully.', 'success')
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