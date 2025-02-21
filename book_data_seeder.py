import os
import sys
import sqlite3
from datetime import datetime

# Add the current directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our models
from data_models import db, Author, Book

# Database configuration - make sure this matches your main app configuration
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'library.sqlite')
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

# Real book data with famous authors and their notable works, including ratings
REAL_BOOK_DATA = [
    # J.K. Rowling - Harry Potter Series
    {
        "author": {
            "name": "J.K. Rowling",
            "birth_date": "1965-07-31"
        },
        "books": [
            {"isbn": "9780590353427", "title": "Harry Potter and the Sorcerer's Stone", "publication_year": 1997, "rating": 9},
            {"isbn": "9780439064873", "title": "Harry Potter and the Chamber of Secrets", "publication_year": 1998, "rating": 9},
            {"isbn": "9780439136365", "title": "Harry Potter and the Prisoner of Azkaban", "publication_year": 1999, "rating": 10},
            {"isbn": "9780439139595", "title": "Harry Potter and the Goblet of Fire", "publication_year": 2000, "rating": 8},
            {"isbn": "9780439358071", "title": "Harry Potter and the Order of the Phoenix", "publication_year": 2003, "rating": 7},
            {"isbn": "9780439784542", "title": "Harry Potter and the Half-Blood Prince", "publication_year": 2005, "rating": 9},
            {"isbn": "9780545010221", "title": "Harry Potter and the Deathly Hallows", "publication_year": 2007, "rating": 10}
        ]
    },

    # George Orwell - Classic Dystopian Novels
    {
        "author": {
            "name": "George Orwell",
            "birth_date": "1903-06-25",
            "date_of_death": "1950-01-21"
        },
        "books": [
            {"isbn": "9780451524935", "title": "1984", "publication_year": 1949, "rating": 10},
            {"isbn": "9780452284340", "title": "Animal Farm", "publication_year": 1945, "rating": 9},
            {"isbn": "9780156186001", "title": "Homage to Catalonia", "publication_year": 1938, "rating": 8},
            {"isbn": "9780156031585", "title": "Down and Out in Paris and London", "publication_year": 1933, "rating": 7}
        ]
    },

    # Add more authors and books here...
]

def parse_date(date_str):
    """Convert string date to date object"""
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return None


def clear_existing_data():
    """Clear all existing data from the database."""
    print("Clearing existing database data...")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS book")
        cursor.execute("DROP TABLE IF EXISTS author")

        conn.commit()
        conn.close()
        print("Database cleared successfully.")
    except Exception as e:
        print(f"Error clearing database: {e}")


def seed_real_books():
    """Seed the database with real book data, including ratings."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Create a database engine and session
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Recreate the tables
        db.metadata.create_all(engine)

        author_count = 0
        book_count = 0

        # Track ISBNs to avoid duplicates
        used_isbns = set()

        for author_data in REAL_BOOK_DATA:
            # Create the author
            author = Author(
                name=author_data["author"]["name"],
                birth_date=parse_date(author_data["author"].get("birth_date")),
                date_of_death=parse_date(author_data["author"].get("date_of_death"))
            )
            session.add(author)
            session.flush()  # Get the author ID without committing
            author_count += 1

            # Add all books by this author
            for book_data in author_data["books"]:
                isbn = book_data["isbn"]

                # Skip if ISBN already used (avoid duplicate key error)
                if isbn in used_isbns:
                    print(f"Warning: Skipping duplicate ISBN {isbn} for '{book_data['title']}'")
                    continue

                used_isbns.add(isbn)

                book = Book(
                    isbn=isbn,
                    title=book_data["title"],
                    publication_year=book_data["publication_year"],
                    author_id=author.id,
                    rating=book_data.get("rating")  # Include the rating field
                )
                session.add(book)
                book_count += 1

        # Commit all changes
        session.commit()
        print(f"Successfully added {author_count} authors and {book_count} books to the database.")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    # Check if the database exists
    if not os.path.exists(DATABASE_PATH):
        print(f"Database file not found at {DATABASE_PATH}. Creating a new one.")
    else:
        # Clear existing data
        clear_existing_data()

    # Seed with real book data
    seed_real_books()