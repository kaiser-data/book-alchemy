# Book-Alchemy Library Management System

A Flask-based web application that allows users to manage their personal library of books and authors. It includes features such as adding, deleting, rating books, and generating AI-based book recommendations.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Add Authors**: Add new authors with their birth date and date of death.
- **Add Books**: Add books with ISBN, title, publication year, and associate them with an author.
- **Delete Books/Authors**: Remove books or authors from the library. Authors are automatically deleted if they have no remaining books.
- **Rate Books**: Rate books on a scale of 1-10 directly from the home page.
- **Search Functionality**: Search for books by title or author name.
- **Sorting Options**: Sort books by title or author name.
- **AI-Based Book Recommendations**: Generate personalized book recommendations based on rated books using an AI API.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.12+
- Flask (`pip install Flask`)
- Flask-SQLAlchemy (`pip install Flask-SQLAlchemy`)
- python-dotenv (`pip install python-dotenv`)
- OpenAI or a compatible AI API (`pip install openai`)

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory and add the following:
     ```
     SECRET_KEY=your_secret_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Initialize the Database**:
   - Run the seeder script to populate the database with real book data:
     ```bash
     python real_book_seeder.py
     ```
   - Optionally, preserve existing data by running:
     ```bash
     python real_book_seeder.py --preserve
     ```

6. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will run on `http://127.0.0.1:5001`.

---

## Usage

1. **Home Page**:
   - View all books in the library.
   - Search for books by title or author name.
   - Sort books by title or author name.
   - Rate books using the dropdown menu.

2. **Book Details**:
   - Click on a book title to view detailed information about the book.

3. **Author Details**:
   - Click on an author's name to view their details and list of books.

4. **Add Books/Authors**:
   - Use the `/add_author` and `/add_book` routes to add new authors and books.

5. **Delete Books/Authors**:
   - Use the delete buttons to remove books or authors from the library.

6. **Get Book Recommendations**:
   - Navigate to `/recommend_book` to generate personalized book recommendations based on your rated books.

---

## Database Schema

The application uses SQLite as the database backend. The schema consists of two tables:

### **Author**
| Column         | Type      | Description                          |
|----------------|-----------|---------------------------------------|
| id             | Integer   | Primary key (auto-incrementing)       |
| name           | String    | Name of the author (required)         |
| birth_date     | Date      | Birth date of the author (optional)   |
| date_of_death  | Date      | Date of death of the author (optional)|
| books          | Relation   | List of books written by the author   |

### **Book**
| Column         | Type      | Description                          |
|----------------|-----------|---------------------------------------|
| id             | Integer   | Primary key (auto-incrementing)       |
| isbn           | String    | ISBN of the book (unique, required)   |
| title          | String    | Title of the book (required)          |
| publication_year| Integer   | Year of publication (required)        |
| author_id      | Integer   | Foreign key referencing Author.id     |
| rating         | Integer   | User rating (1-10, optional)          |

---

## API Integration

The application integrates with an AI API to generate book recommendations. By default, it uses the OpenAI API with the following configuration:

- **Base URL**: `https://api.aimlapi.com/v1`
- **Model**: `meta-llama/Llama-2-13b-chat-hf` (or another supported model)

Ensure you have a valid API key and update the `.env` file accordingly.

---

## Contributing

To contribute to this project:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes and commit them: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License.
