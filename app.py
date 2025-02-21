import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from data_models import db, Author, Book
from datetime import datetime
import sqlalchemy
from dotenv import load_dotenv

import os
import openai


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key')

# Configure database
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'library.sqlite')
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

# Helper function for date conversion
def parse_date(date_str):
    """Converts a string to a Date object if valid, otherwise returns None."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except ValueError:
        return None

# Routes

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page route that shows all books with optional sorting, keyword search, and rating functionality."""
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        rating = request.form.get('rating')
        if book_id and rating:
            try:
                book = Book.query.get_or_404(book_id)
                book.rating = int(rating) if 1 <= int(rating) <= 10 else None
                db.session.commit()
                flash(f'Rating for "{book.title}" updated successfully.', 'success')
            except Exception as e:
                flash(f'Error updating rating: {str(e)}', 'error')

    sort_by = request.args.get('sort_by', 'title')  # Default sorting by title
    search_query = request.args.get('search', '').strip()  # Get the search query

    if search_query:
        books = Book.query.filter(
            (Book.title.ilike(f"%{search_query}%")) |
            (Author.name.ilike(f"%{search_query}%"))
        ).join(Author).all()
    else:
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name.asc()).all()
        else:  # Default to title sorting
            books = Book.query.order_by(Book.title.asc()).all()

    authors = Author.query.order_by(Author.name.asc()).all()
    return render_template('home.html', books=books, authors=authors, search_query=search_query)


@app.route('/add_author', methods=['POST'])
def add_author():
    """Add a new author to the database."""
    name = request.form.get('name')
    birth_date = parse_date(request.form.get('birth_date'))
    date_of_death = parse_date(request.form.get('date_of_death'))

    if not name:
        flash('Author name is required', 'error')
        return redirect(url_for('home'))

    try:
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
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    publication_year = request.form.get('publication_year')
    author_id = request.form.get('author_id')

    if not all([isbn, title, publication_year, author_id]):
        flash('All fields are required', 'error')
        return redirect(url_for('home'))

    try:
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


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book and optionally its author if no other books remain."""
    book = Book.query.get_or_404(book_id)

    try:
        db.session.delete(book)
        db.session.commit()

        # Delete the author if they have no remaining books
        author = Author.query.get(book.author_id)
        if author and not author.books:
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
    author = Author.query.get_or_404(author_id)

    try:
        db.session.delete(author)
        db.session.commit()
        flash(f'Author "{author.name}" and all their books deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting author: {str(e)}', 'error')

    return redirect(url_for('home'))


@app.route('/book/<int:book_id>')
def book_details(book_id):
    """Display detailed information about a specific book."""
    book = Book.query.get_or_404(book_id)  # Ensure the book exists, or return a 404 error
    return render_template('book.html', book=book)

@app.route('/author/<int:author_id>')
def author_details(author_id):
    """Display detailed information about a specific author."""
    author = Author.query.get_or_404(author_id)  # Ensure the author exists, or return a 404 error
    return render_template('author.html', author=author)


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded correctly
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI")

openai.base_url = "https://api.aimlapi.com/v1"

@app.route('/recommend_book', methods=['GET'])
def recommend_book():
    """Generate a book recommendation using AI."""
    books_read = Book.query.filter(Book.rating.isnot(None)).all()  # Get books with ratings
    if not books_read:
        flash('You need to rate some books first!', 'info')
        return redirect(url_for('home'))

    # Prepare the prompt for ChatGPT
    prompt = "Based on the following books I've read:\n"
    for book in books_read:
        prompt += f"- '{book.title}' by {book.author.name}, rated {book.rating}/10\n"
    prompt += "\nRecommend a new book for me to read."

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": "You are a helpful book recommendation assistant."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": ""}
            ],
            temperature=0.7,
            max_tokens=256,
        )
        recommendation = response.choices[0].message.content.strip()
    except Exception as e:
        recommendation = f"Error generating recommendation: {str(e)}"

    return render_template('recommendation.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))