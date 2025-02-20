from flask_sqlalchemy import SQLAlchemy

# Create a db object to be used in the models
db = SQLAlchemy()

# Define the Author model
class Author(db.Model):
    __tablename__ = 'author'

    # Columns for the Author model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    name = db.Column(db.String(100), nullable=False)  # Name of the author (required)
    birth_date = db.Column(db.Date, nullable=True)  # Birth date of the author (optional)
    date_of_death = db.Column(db.Date, nullable=True)  # Date of death of the author (optional)

    # Relationship with the Book model
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        """Custom representation for debugging purposes."""
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """Custom string representation for meaningful output."""
        return f"Author: {self.name}"

# Define the Book model
class Book(db.Model):
    __tablename__ = 'book'

    # Columns for the Book model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    isbn = db.Column(db.String(20), unique=True, nullable=False)  # ISBN of the book (unique and required)
    title = db.Column(db.String(150), nullable=False)  # Title of the book (required)
    publication_year = db.Column(db.Integer, nullable=False)  # Publication year of the book (required)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)  # Foreign key to the Author table

    def __repr__(self):
        """Custom representation for debugging purposes."""
        return f"<Book(id={self.id}, title='{self.title}', author_id={self.author_id})>"

    def __str__(self):
        """Custom string representation for meaningful output."""
        return f"Book: {self.title} by {self.author.name if self.author else 'Unknown'}"

# Uncomment this block only when you want to create the tables initially
# from app import app  # Import the Flask app instance
# with app.app_context():
#     db.create_all()