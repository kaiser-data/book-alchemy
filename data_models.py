from flask_sqlalchemy import SQLAlchemy

# Create a db object to be used in the models
db = SQLAlchemy()

# Define the Author model
class Author(db.Model):
    __tablename__ = 'author'

    # Columns for the Author model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Relationship with the Book model
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        """Custom representation for debugging purposes."""
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """Custom string representation for meaningful output."""
        return self.name


# Define the Book model
class Book(db.Model):
    __tablename__ = 'book'

    # Columns for the Book model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        """Custom representation for debugging purposes."""
        return f"<Book(id={self.id}, title='{self.title}', author_id={self.author_id})>"

    def __str__(self):
        """Custom string representation for meaningful output."""
        return f"{self.title}"