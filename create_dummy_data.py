# real_book_seeder.py - Fixed Version
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

# Real book data with famous authors and their notable works - Fixed ISBN issues
REAL_BOOK_DATA = [
    # J.K. Rowling - Harry Potter Series
    {
        "author": {
            "name": "J.K. Rowling",
            "birth_date": "1965-07-31"
        },
        "books": [
            {"isbn": "9780590353427", "title": "Harry Potter and the Sorcerer's Stone", "publication_year": 1997},
            {"isbn": "9780439064873", "title": "Harry Potter and the Chamber of Secrets", "publication_year": 1998},
            {"isbn": "9780439136365", "title": "Harry Potter and the Prisoner of Azkaban", "publication_year": 1999},
            {"isbn": "9780439139595", "title": "Harry Potter and the Goblet of Fire", "publication_year": 2000},
            {"isbn": "9780439358071", "title": "Harry Potter and the Order of the Phoenix", "publication_year": 2003},
            {"isbn": "9780439784542", "title": "Harry Potter and the Half-Blood Prince", "publication_year": 2005},
            {"isbn": "9780545010221", "title": "Harry Potter and the Deathly Hallows", "publication_year": 2007}
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
            {"isbn": "9780451524935", "title": "1984", "publication_year": 1949},
            {"isbn": "9780452284241", "title": "Animal Farm", "publication_year": 1945},
            {"isbn": "9780156186001", "title": "Homage to Catalonia", "publication_year": 1938},
            {"isbn": "9780156031585", "title": "Down and Out in Paris and London", "publication_year": 1933}
        ]
    },

    # Jane Austen - Classic Romance Novels
    {
        "author": {
            "name": "Jane Austen",
            "birth_date": "1775-12-16",
            "date_of_death": "1817-07-18"
        },
        "books": [
            {"isbn": "9780141439518", "title": "Pride and Prejudice", "publication_year": 1813},
            {"isbn": "9780141439587", "title": "Sense and Sensibility", "publication_year": 1811},
            {"isbn": "9780141439778", "title": "Emma", "publication_year": 1815},
            {"isbn": "9780141439891", "title": "Persuasion", "publication_year": 1817},
            {"isbn": "9780141439709", "title": "Mansfield Park", "publication_year": 1814},
            {"isbn": "9780141441146", "title": "Northanger Abbey", "publication_year": 1818}
        ]
    },

    # Ernest Hemingway - Literary Classics
    {
        "author": {
            "name": "Ernest Hemingway",
            "birth_date": "1899-07-21",
            "date_of_death": "1961-07-02"
        },
        "books": [
            {"isbn": "9780684801223", "title": "The Old Man and the Sea", "publication_year": 1952},
            {"isbn": "9780684843131", "title": "A Farewell to Arms", "publication_year": 1929},
            {"isbn": "9780684824994", "title": "For Whom the Bell Tolls", "publication_year": 1940},
            {"isbn": "9780684836973", "title": "The Sun Also Rises", "publication_year": 1926}
        ]
    },

    # Agatha Christie - Mystery Novels
    {
        "author": {
            "name": "Agatha Christie",
            "birth_date": "1890-09-15",
            "date_of_death": "1976-01-12"
        },
        "books": [
            {"isbn": "9780062073488", "title": "Murder on the Orient Express", "publication_year": 1934},
            {"isbn": "9780062073945", "title": "And Then There Were None", "publication_year": 1939},
            {"isbn": "9780062073556", "title": "Death on the Nile", "publication_year": 1937},
            {"isbn": "9780062073723", "title": "The Murder of Roger Ackroyd", "publication_year": 1926},
            {"isbn": "9780062073822", "title": "The ABC Murders", "publication_year": 1936}
        ]
    },

    # Gabriel García Márquez - Magical Realism
    {
        "author": {
            "name": "Gabriel García Márquez",
            "birth_date": "1927-03-06",
            "date_of_death": "2014-04-17"
        },
        "books": [
            {"isbn": "9780060883287", "title": "One Hundred Years of Solitude", "publication_year": 1967},
            {"isbn": "9781400034680", "title": "Love in the Time of Cholera", "publication_year": 1985},
            {"isbn": "9780679755906", "title": "Chronicle of a Death Foretold", "publication_year": 1981},
            {"isbn": "9781400034925", "title": "The Autumn of the Patriarch", "publication_year": 1975}
        ]
    },

    # Toni Morrison - American Literature
    {
        "author": {
            "name": "Toni Morrison",
            "birth_date": "1931-02-18",
            "date_of_death": "2019-08-05"
        },
        "books": [
            {"isbn": "9781400033416", "title": "Beloved", "publication_year": 1987},
            {"isbn": "9781400033430", "title": "Song of Solomon", "publication_year": 1977},
            {"isbn": "9780307388629", "title": "The Bluest Eye", "publication_year": 1970},
            {"isbn": "9781400076215", "title": "Paradise", "publication_year": 1997}
        ]
    },

    # Haruki Murakami - Contemporary Fiction
    {
        "author": {
            "name": "Haruki Murakami",
            "birth_date": "1949-01-12"
        },
        "books": [
            {"isbn": "9780307476463", "title": "Norwegian Wood", "publication_year": 1987},
            {"isbn": "9780679775430", "title": "The Wind-Up Bird Chronicle", "publication_year": 1994},
            {"isbn": "9780375704024", "title": "Kafka on the Shore", "publication_year": 2002},
            {"isbn": "9780307593313", "title": "1Q84", "publication_year": 2009}  # Fixed duplicate ISBN
        ]
    },

    # F. Scott Fitzgerald - American Classics
    {
        "author": {
            "name": "F. Scott Fitzgerald",
            "birth_date": "1896-09-24",
            "date_of_death": "1940-12-21"
        },
        "books": [
            {"isbn": "9780743273565", "title": "The Great Gatsby", "publication_year": 1925},
            {"isbn": "9780684830421", "title": "Tender Is the Night", "publication_year": 1934},
            {"isbn": "9780684843780", "title": "This Side of Paradise", "publication_year": 1920},
            {"isbn": "9780684824482", "title": "The Beautiful and Damned", "publication_year": 1922}
        ]
    },

    # Virginia Woolf - Modernist Literature
    {
        "author": {
            "name": "Virginia Woolf",
            "birth_date": "1882-01-25",
            "date_of_death": "1941-03-28"
        },
        "books": [
            {"isbn": "9780156030359", "title": "Mrs. Dalloway", "publication_year": 1925},
            {"isbn": "9780156907392", "title": "To the Lighthouse", "publication_year": 1927},
            {"isbn": "9780156028059", "title": "Orlando", "publication_year": 1928},
            {"isbn": "9780156949606", "title": "A Room of One's Own", "publication_year": 1929}
        ]
    },

    # Leo Tolstoy - Russian Literature
    {
        "author": {
            "name": "Leo Tolstoy",
            "birth_date": "1828-09-09",
            "date_of_death": "1910-11-20"
        },
        "books": [
            {"isbn": "9780143035003", "title": "War and Peace", "publication_year": 1869},
            {"isbn": "9780143035008", "title": "Anna Karenina", "publication_year": 1877},  # Fixed duplicate ISBN
            {"isbn": "9780140449174", "title": "The Death of Ivan Ilyich", "publication_year": 1886},
            {"isbn": "9780140444414", "title": "Resurrection", "publication_year": 1899}
        ]
    },

    # Margaret Atwood - Contemporary Literature
    {
        "author": {
            "name": "Margaret Atwood",
            "birth_date": "1939-11-18"
        },
        "books": [
            {"isbn": "9780385490818", "title": "The Handmaid's Tale", "publication_year": 1985},
            {"isbn": "9780385721677", "title": "Oryx and Crake", "publication_year": 2003},
            {"isbn": "9780385720953", "title": "The Blind Assassin", "publication_year": 2000},
            {"isbn": "9780385528771", "title": "The Testaments", "publication_year": 2019}
        ]
    },

    # James Baldwin - American Essays and Fiction
    {
        "author": {
            "name": "James Baldwin",
            "birth_date": "1924-08-02",
            "date_of_death": "1987-12-01"
        },
        "books": [
            {"isbn": "9780345806543", "title": "Go Tell It on the Mountain", "publication_year": 1953},
            {"isbn": "9780679744719", "title": "Giovanni's Room", "publication_year": 1956},
            {"isbn": "9780679761785", "title": "Another Country", "publication_year": 1962},
            {"isbn": "9780679744726", "title": "The Fire Next Time", "publication_year": 1963}
        ]
    },

    # Chimamanda Ngozi Adichie - Contemporary Fiction
    {
        "author": {
            "name": "Chimamanda Ngozi Adichie",
            "birth_date": "1977-09-15"
        },
        "books": [
            {"isbn": "9781400095209", "title": "Half of a Yellow Sun", "publication_year": 2006},
            {"isbn": "9780307455925", "title": "Americanah", "publication_year": 2013},
            {"isbn": "9781400076239", "title": "Purple Hibiscus", "publication_year": 2003},
            {"isbn": "9780307962027", "title": "We Should All Be Feminists", "publication_year": 2014}
        ]
    },

    # J.R.R. Tolkien - Fantasy Literature
    {
        "author": {
            "name": "J.R.R. Tolkien",
            "birth_date": "1892-01-03",
            "date_of_death": "1973-09-02"
        },
        "books": [
            {"isbn": "9780618640157", "title": "The Hobbit", "publication_year": 1937},
            {"isbn": "9780618346257", "title": "The Fellowship of the Ring", "publication_year": 1954},
            {"isbn": "9780618346264", "title": "The Two Towers", "publication_year": 1954},
            {"isbn": "9780618346271", "title": "The Return of the King", "publication_year": 1955},
            {"isbn": "9780618391110", "title": "The Silmarillion", "publication_year": 1977}
        ]
    }
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

        # Check if tables exist before attempting to delete
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='book'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM book")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='author'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM author")

        # Only attempt to reset sequence if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='book' OR name='author'")

        conn.commit()
        conn.close()
        print("Database cleared successfully")
    except Exception as e:
        print(f"Error clearing database: {e}")


def seed_real_books():
    """Seed the database with real book data."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Create a database engine and session
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
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
                    author_id=author.id
                )
                session.add(book)
                book_count += 1

        # Commit all changes
        session.commit()
        print(f"Successfully added {author_count} authors and {book_count} books to the database")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        # Print more detailed error info
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    # Check if the database exists
    if not os.path.exists(DATABASE_PATH):
        print(f"Database file not found at {DATABASE_PATH}")
        print("Please run your main application once to initialize the database schema.")
        sys.exit(1)

    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Seed the library database with real book data")
    parser.add_argument("--preserve", action="store_true", help="Preserve existing data")
    args = parser.parse_args()

    # Clear existing data unless preserve flag is set
    if not args.preserve:
        clear_existing_data()

    # Seed with real book data
    seed_real_books()