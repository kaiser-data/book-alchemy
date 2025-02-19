from flask import Flask
import os
import sqlalchemy
from data_models import db, Author, Book

# Initialize the Flask application
app = Flask(__name__)

# Define the database file path
database_file = "data/library.sqlite"
database_path = f"sqlite:///{os.path.abspath(database_file)}"  # Use absolute path for clarity

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(os.path.abspath(database_file)), exist_ok=True)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance



# Define models (if not already defined in a separate module)
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

# Create all tables within the application context
with app.app_context():
    try:
        print(f"Database file path: {os.path.abspath(database_file)}")  # Print the absolute path for debugging
        if not os.path.exists(os.path.abspath(database_file)):
            print(f"Database file '{database_file}' does not exist. Creating it...")

        db.create_all()
        print("Database and tables have been initialized successfully.")
    except sqlalchemy.exc.OperationalError as e:
        print(f"Error initializing the database: {e}")
        print("Possible causes:")
        print("- The application may not have write permissions to the directory.")
        print("- The specified path may be incorrect or inaccessible.")
        print(f"- Absolute path used: {os.path.abspath(database_file)}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Optional: Add routes or other application logic here
@app.route('/')
def index():
    return "Library Management System"

if __name__ == '__main__':
    app.run(debug=True)